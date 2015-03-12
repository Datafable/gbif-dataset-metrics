from glob import glob
import json
import random
import requests
from dateutil import parser
from nesting import Nest

class ReportAggregator():
    """
    This class will be used to aggregate *.json files.
    Metric data will be aggregated by data set key
    """

    def find_files(self, folder):
        """
        Look for all *.json files
        in a given folder.
        """
        files = glob(folder + '/*.json')
        return files

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
            if metric_type in metrics_data.keys() and metric_type is not 'ARCHIVE_GENERATED_AT':
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
                

    def aggregate(self, data_folder):
        """
        iterate over all the *.json files
        and merge the metrics data by dataset key and
        metric type.
        Once the aggregation is finished, create a taxonomy tree
        and create a sample of image urls.
        """
        files = self.find_files(data_folder)
        metrics = {}
        for f in files:
            print 'aggregating {0}'.format(f)
            data = json.load(open(f))
            for data_set in data.keys():
                if data_set in metrics.keys():
                    self.merge_data_set_in_metrics(data[data_set], metrics[data_set])
                else:
                    metrics[data_set] = data[data_set]
        for dataset in metrics.keys():
            taxonomy = self.aggregate_taxonomy(metrics[dataset]['TAXONOMY'])
            metrics[dataset]['TAXONOMY'] = taxonomy
            if 'MEDIA' in metrics[dataset].keys():
                images_sample = self.get_images_sample(metrics[dataset]['MEDIA'], 20)
                metrics[dataset]['MEDIA']['images_sample'] = json.dumps(images_sample)
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
        self.sql_statement = "update gbif_dataset_metrics_test set bor_preserved_specimen={0}, bor_fossil_specimen={1}, bor_living_specimen={2}, bor_material_sample={3}, bor_observation={4}, bor_human_observation={5}, bor_machine_observation={6}, bor_literature={7}, bor_unknown={8}, taxon_not_provided={9}, taxon_match_none={10}, taxon_match_higherrank={11}, taxon_match_fuzzy={12}, taxon_match_complete={13}, multimedia_not_provided={14}, multimedia_url_invalid={15}, multimedia_valid={16}, coordinates_not_provided={17}, coordinates_minor_issues={18}, coordinates_major_issues={19}, coordinates_valid={20}, occurrences={21}, taxonomy='{22}', images_sample='{23}', archive_generated_at='{24}' where dataset_key='{25}'; insert into gbif_dataset_metrics_test (type, bor_preserved_specimen, bor_fossil_specimen, bor_living_specimen, bor_material_sample, bor_observation, bor_human_observation, bor_machine_observation, bor_literature, bor_unknown, taxon_not_provided, taxon_match_none, taxon_match_higherrank, taxon_match_fuzzy, taxon_match_complete, multimedia_not_provided, multimedia_url_invalid, multimedia_valid, coordinates_not_provided, coordinates_minor_issues, coordinates_major_issues, coordinates_valid, occurrences, taxonomy, images_sample, archive_generated_at, dataset_key) SELECT 'OCCURRENCE', {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, '{22}', '{23}', '{24}', '{25}' WHERE NOT EXISTS (SELECT 1 FROM gbif_dataset_metrics_test WHERE dataset_key='{25}')"

    def write_metrics(self, row, api_key):
        params = {'q': self.sql_statement.format(*row), 'api_key': api_key}
        #print self.sql_statement.format(*row)
        r = requests.post('http://datafable.cartodb.com/api/v2/sql', data=params)
        print r.status_code
        print r.text
