from glob import glob
import json
import pickle
import os
import re
import random
import requests
import logging
from nesting import Nest

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

class AggregationJobsManager():

    def find_files(self, folder):
        """
        Look for all *.json files
        in a given folder.
        """
        files = glob(folder + '/*.json')
        return files

    def createIndex(self, folder):
        """
        The index contains an array of files that contain metrics
        for a given dataset, per dataset key. This means that if
        you need all the metrics for one dataset, you can use the
        index to find out which files you need to open.
        """
        index_file_name = os.path.join(folder, 'dataset_index.pkl')
        if os.path.exists(index_file_name):
            index = pickle.load(open(index_file_name))
            if len(index.keys()) > 0:
                logging.debug('reading existing index')
                logging.debug('index contains {0} datasets'.format(len(index.keys())))
                return index
        logging.debug('creating index')
        files = self.find_files(folder)
        index = {}
        for f in files:
            data = json.load(open(f))
            for data_set in data.keys():
                if data_set in index.keys():
                    index[data_set].append(f)
                else:
                    index[data_set] = [f]
        index_file = open(index_file_name, 'w+')
        pickle.dump(index, index_file)
        logging.debug('index created')
        logging.debug('index contains {0} datasets'.format(len(index.keys())))
        return index


    def aggregate(self, data_folder, api_key=None, minindex=0, limit=None):
        """
        iterate over all the *.json files
        and merge the metrics data by dataset key and
        metric type.
        Once the aggregation is finished, create a taxonomy tree
        and create a sample of image urls.
        """
        index = self.createIndex(data_folder)
        sorted_datasets = sorted(index.keys())
        outfile = open('agg_data.json', 'w+')
        outfile.write('{')
        separator = ''
        if limit is None:
            limit = len(sorted_datasets) - minindex
            maxindex = len(sorted_datasets)
        else:
            if limit > len(sorted_datasets) - minindex:
                limit = len(sorted_datasets) - minindex
            maxindex = limit + minindex
        logging.debug('{0} datasets to process'.format(limit))
        for x in sorted_datasets[minindex:maxindex]:
            subindex = {'index': [x, index[x]], 'api_key': api_key}
            r = ReportAggregator()
            metrics = r.aggregate_dataset(subindex)
            if api_key is None:
                outfile.write(separator)
                separator = ','
                outfile.write('"{0}": '.format(x))
                json.dump(metrics, outfile)
        outfile.write('}')
        outfile.close()


class ReportAggregator():
    """
    This class will be used to aggregate *.json files.
    Metric data will be aggregated by data set key
    """

    def merge_data_set_in_metrics(self, dataset, metrics_data):
        """
        merge the metric data by metric type and metric name and return
            a new outdata object. Merging should follow these rules:
                - if the value of a key is not a dict, return the sum of the values for this
                  key in newdata and outdata.
                - if the value of key is a dict, check every key in that dict and:
                    - if the value is not a dict, return the sum
                    - if the value is a dict, add every key and value from newdata to outdata
                        (logically, duplicate keys cannot occur)
        """
        for metric_type in dataset.keys():
            if metric_type in metrics_data.keys() and not re.search('ARCHIVE_GENERATED_AT', metric_type):
                if type(dataset[metric_type]) is dict:
                    for metric_name in dataset[metric_type].keys():
                        if metric_name in ['audio', 'no_type', 'movingimage', 'stillimage'] and metric_type is 'MEDIA':
                            pass # Skip the multimedia. We will not use it at this point and it's consuming lots of resources
                        else:
                            if type(dataset[metric_type][metric_name]) is dict:
                                for occurrence_id in dataset[metric_type][metric_name].keys():
                                    metrics_data[metric_type][metric_name][occurrence_id] = dataset[metric_type][metric_name][occurrence_id]
                            else:
                                if metric_name in metrics_data[metric_type].keys():
                                    metrics_data[metric_type][metric_name] += dataset[metric_type][metric_name]
                                else:
                                    metrics_data[metric_type][metric_name] = dataset[metric_type][metric_name]
                else:
                    metrics_data[metric_type] += dataset[metric_type]
            else:
                metrics_data[metric_type] = dataset[metric_type]
        return True
                

    def aggregate_dataset(self, data):
        index = data['index']
        api_key = data['api_key']
        dataset_key = index[0]
        files = index[1]
        metrics = {}
        for f in files:
            data = json.load(open(f))
            if metrics is {}:
                metrics = data[dataset_key]
            else:
                self.merge_data_set_in_metrics(data[dataset_key], metrics)
        taxonomy = self.aggregate_taxonomy(metrics['TAXONOMY'])
        metrics['TAXONOMY'] = taxonomy
        if 'MEDIA' in metrics.keys():
            images_sample = self.get_images_sample(metrics['MEDIA'], 20)
            metrics['MEDIA']['images_sample'] = json.dumps(images_sample)
        if api_key is not None:
            writer = CartoDBWriter()
            writer.write_metrics(dataset_key, metrics, api_key)
        logging.debug('dataset {0} processed'.format(dataset_key))
        return metrics

    def get_images_sample(self, indata, sample_size):
        """
        Select images from occurrences randomly. From all occurrences
        that have at least one image url, a number of occurrences that
        equals `sample_size` is selected at random. For each occurrence,
        one image url is randomly selected resulting in an output like
            {
                'occurrenceid1': 'image_url_1',
                'occurrenceid2': 'image_url_2'
            }
        """
        images_sample = {}
        all_images = indata['stillimage']
        if len(all_images.keys()) is 0:
            all_images = indata['no_type']
            if len(all_images.keys()) is 0:
                return None
        occurrences = all_images.keys()
        random.shuffle(occurrences)
        occ_sample = occurrences[0:sample_size]
        for occ in occ_sample:
            occ_images = all_images[occ]
            random.shuffle(occ_images)
            images_sample[occ] = occ_images[0]
        return images_sample

    def _get_sum(self, arr):
        """
        sum all last elements or an array of arrays
        """
        return sum([int(x[-1]) for x in arr])

    def _taxonkey_to_array(self, taxonkey):
        """
        The taxonkey in the output of the extractor has the format:
            'taxon1|taxon2|taxon3|...'
        where every subsequent taxon is a subtaxon of the previous taxon.
        _taxonkey_to_array splits these keys and returns an array of the
        taxa. If a taxon is not named (there is an empty string), then 
        'Unknown' is returned for that taxon.
        """
        taxa = taxonkey.split('|')
        outtaxa = ['Unknown' if x is None or x is '' or x is u'' else x for x in taxa]
        if len(taxa) < 7:
            for i in range(7 - len(outtaxa)):
                outtaxa.append('Unknown')
        return outtaxa

    def _tree_to_dict(self, intree):
        """
        convert a taxonomic tree (as a dict) to something like:
            {
            'name': 'taxon1'
            'children': [{
                'name': 'species1',
                'size': 425
                ...
            }]
            }
        """
        outtree = []
        taxa = intree.keys()
        taxa.sort()
        for taxon in taxa:
            try:
                val = int(intree[taxon])
                outtree.append({'name': taxon, 'size': val})
            except:
                subtree = self._tree_to_dict(intree[taxon])
                outtree.append({'name': taxon, 'children': subtree})
        outtree.sort()
        return outtree

    def aggregate_taxonomy(self, input_taxonomy, do_genus=True, do_species=True):
        """
        create a dict containing taxonomic information from a dict where each
        key represents one taxon (including the higher taxonomy in the key)
        and each value is the number of occurrences for this taxon in the
        dataset.
        First, each key will be split, and an array of arrays will be created.
        The arrays should be grouped by:
            - kingdom (index 0)
            - phylum (index 1)
            - class (index 2)
            - order (index 3)
            - family (index 4)
            - genus (index 5, optional)
            - species (index 6, optional)
        The last element of every array should be the count.
        All counts of all the remaining arrays in each leave are
        summed.
        """
        taxonomy_arrays = [self._taxonkey_to_array(x) + [input_taxonomy[x]] for x in input_taxonomy.keys()]
        if len(taxonomy_arrays) > 1000:
            do_species=False
            if len(taxonomy_arrays) > 5000:
                do_genus=False
        if do_genus and do_species:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).key(lambda d: d[6]).rollup(self._get_sum).map(taxonomy_arrays)
        elif do_genus and not do_species:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).rollup(self._get_sum).map(taxonomy_arrays)
        else:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).rollup(self._get_sum).map(taxonomy_arrays)
        return {'name': 'All taxa', 'children': self._tree_to_dict(agg_taxonomy)}

class CartoDBWriter():
    def __init__(self):
        self.sql_statement = """
        update gbif_dataset_metrics_test
        set bor_preserved_specimen={0}, bor_fossil_specimen={1}, bor_living_specimen={2}, bor_material_sample={3},
        bor_observation={4}, bor_human_observation={5}, bor_machine_observation={6}, bor_literature={7},
        bor_unknown={8}, taxon_not_provided={9}, taxon_match_none={10}, taxon_match_higherrank={11},
        taxon_match_fuzzy={12}, taxon_match_complete={13}, multimedia_not_provided={14}, multimedia_url_invalid={15},
        multimedia_valid={16}, coordinates_not_provided={17}, coordinates_minor_issues={18},
        coordinates_major_issues={19}, coordinates_valid={20}, occurrences={21}, taxonomy='{22}', images_sample={23},
        archive_generated_at='{24}' where dataset_key='{25}';
        insert into gbif_dataset_metrics_test (
            type, bor_preserved_specimen, bor_fossil_specimen, bor_living_specimen, bor_material_sample,
            bor_observation, bor_human_observation, bor_machine_observation, bor_literature, bor_unknown,
            taxon_not_provided, taxon_match_none, taxon_match_higherrank, taxon_match_fuzzy, taxon_match_complete,
            multimedia_not_provided, multimedia_url_invalid, multimedia_valid, coordinates_not_provided,
            coordinates_minor_issues, coordinates_major_issues, coordinates_valid, occurrences, taxonomy, images_sample,
            archive_generated_at, dataset_key
        ) SELECT 'OCCURRENCE', {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15},
        {16}, {17}, {18}, {19}, {20}, {21}, '{22}', {23}, '{24}', '{25}'
        WHERE NOT EXISTS (
            SELECT 1 FROM gbif_dataset_metrics_test WHERE dataset_key='{25}'
        )"""

    def metrics2row(self, metrics):
        basis_of_records_metrics = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE',
                                    'OBSERVATION', 'HUMAN_OBSERVATION', 'MACHINE_OBSERVATION', 'LITERATURE', 'UNKNOWN']
        taxon_match_metrics = ['TAXON_NOT_PROVIDED', 'TAXON_MATCH_NONE', 'TAXON_MATCH_HIGHERRANK', 'TAXON_MATCH_FUZZY',
                               'TAXON_MATCH_COMPLETE']
        media_metrics = ['media_not_provided', 'media_url_invalid', 'media_valid']
        coordinate_metrics = ['COORDINATES_NOT_PROVIDED', 'COORDINATES_MINOR_ISSUES', 'COORDINATES_MAJOR_ISSUES',
                              'COORDINATES_VALID']
        basis_of_records = metrics['BASISOFRECORDS']
        taxon_match = metrics['TAXON_MATCHES']
        media_metr = metrics['MEDIA']
        coordinate_quality = metrics['COORDINATE_QUALITY_CATEGORIES']
        basis_of_record_data = [basis_of_records[x] if x in basis_of_records.keys() else 0 for x in basis_of_records_metrics]
        taxon_match_data = [taxon_match[x] if x in taxon_match.keys() else 0 for x in taxon_match_metrics]
        media_data = [media_metr[x] if x in media_metr.keys() else 0 for x in media_metrics]
        coordinate_quality_data = [coordinate_quality[x] if x in coordinate_quality.keys() else 0 for x in coordinate_metrics]
        nr_of_records = metrics['NUMBER_OF_RECORDS']
        taxonomy = json.dumps(metrics['TAXONOMY'])
        images_sample = metrics['MEDIA']['images_sample']
        archive_generated_date = metrics['ARCHIVE_GENERATED_AT']
        row = basis_of_record_data + taxon_match_data + media_data + coordinate_quality_data + [nr_of_records, taxonomy, images_sample, archive_generated_date]
        return row

    def write_metrics(self, dataset_key, metrics, api_key):
        row = self.metrics2row(metrics)
        row.append(dataset_key)
        params = {'q': self.sql_statement.format(*row), 'api_key': api_key}
        #print self.sql_statement.format(*row)
        r = requests.post('http://datafable.cartodb.com/api/v2/sql', data=params)
        logging.debug('{0}: {1}: {2}'.format(dataset_key, r.status_code, r.text))
