from glob import glob
import json
import requests
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
        merge the metric data by metric type and metric name
        """
        for metric_type in dataset.keys():
            if metric_type in metrics_data.keys():
                if type(dataset[metric_type]) is dict:
                    for metric_name in dataset[metric_type].keys():
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
        metric type
        """
        files = self.find_files(data_folder)
        metrics = {}
        for f in files:
            data = json.load(open(f))
            for data_set in data.keys():
                if data_set in metrics.keys():
                    self.merge_data_set_in_metrics(data[data_set], metrics[data_set])
                else:
                    metrics[data_set] = data[data_set]
        for dataset in metrics.keys():
            taxonomy = self.aggregate_taxonomy(metrics[dataset]['TAXONOMY'])
            metrics[dataset]['TAXONOMY'] = taxonomy
        return metrics

    def _get_sum(self, arr):
        """
        sum all last elements or an array of arrays
        """
        return sum([int(x[-1]) for x in arr])

    def _taxonkey_to_array(self, taxonkey):
        taxa = taxonkey.split('|')
        if len(taxa) < 7:
            for i in range(7 - len(taxa)):
                taxa.append('unknown')
        return taxa

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
        if do_genus and do_species:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).key(lambda d: d[6]).rollup(self._get_sum).map(taxonomy_arrays)
        elif do_genus and not do_species:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).rollup(self._get_sum).map(taxonomy_arrays)
        else:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).rollup(self._get_sum).map(taxonomy_arrays)
        return {'name': 'all taxa', 'children': self._tree_to_dict(agg_taxonomy)}

class CartoDBWriter():
    def __init__(self):
        self.metrics_sql_statement = "delete from gbif_dataset_metrics where dataset_key='{0}'; insert into gbif_dataset_metrics ( dataset_key, bor_preserved_specimen, bor_fossil_specimen, bor_living_specimen, bor_material_sample, bor_observation, bor_human_observation, bor_machine_observation, bor_literature, bor_unknown, taxon_not_provided, taxon_match_none, taxon_match_higherrank, taxon_match_fuzzy, taxon_match_complete, occurrences) values ('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15})"
        self.taxonomy_sql_statement = "update gbif_dataset_metrics set taxonomy='{0}' where dataset_key='{1}'"

    def write_metrics(self, row, api_key):
        params = {'q': self.metrics_sql_statement.format(*row), 'api_key': api_key}
        print self.metrics_sql_statement.format(*row)
        r = requests.get('http://datafable.cartodb.com/api/v2/sql', params=params)
        print r.status_code

    def writeTaxonomy(self, dataset_key, taxonomy_for_this_dataset, api_key):
        params = {'q': self.taxonomy_sql_statement.format(taxonomy_for_this_dataset, dataset_key), 'api_key': api_key}
        r = requests.post('http://datafable.cartodb.com/api/v2/sql', data=params)
        #print r.status_code
        #print r.content
