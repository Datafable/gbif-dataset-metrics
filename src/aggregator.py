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
        return metrics

    def _get_sum(self, arr):
        """
        sum all last elements or an array of arrays
        """
        return sum([x[-1] for x in arr])

    def aggregate_taxonomy(self, taxonomy_arrays, do_genus=True, do_species=True):
        """
        create a taxonomic tree from an array of arrays containing
        taxonomy data.
        The arrays should be grouped by:
            - dataset (index 0)
            - kingdom (index 1)
            - phylum (index 2)
            - class (index 3)
            - order (index 4)
            - family (index 5)
            - genus (index 6, optional)
            - species (index 7, optional)
        The last element of every array should be the count.
        All counts of all the remaining arrays in each leave are
        summed.
        """
        if do_genus and do_species:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).key(lambda d: d[6]).key(lambda d: d[7]).rollup(self._get_sum).map(taxonomy_arrays)
        elif do_genus and not do_species:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).key(lambda d: d[6]).rollup(self._get_sum).map(taxonomy_arrays)
        else:
            agg_taxonomy = Nest().key(lambda d: d[0]).key(lambda d: d[1]).key(lambda d: d[2]).key(lambda d: d[3]).key(lambda d: d[4]).key(lambda d: d[5]).rollup(self._get_sum).map(taxonomy_arrays)
        return json.dumps(agg_taxonomy)

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
        params = {'q': self.taxonomy_sql_statement.format(dataset_key, taxonomy_for_this_dataset), 'api_key': api_key}
        print self.taxonomy_sql_statement.format(taxonomy_for_this_dataset, dataset_key)
        r = requests.post('http://datafable.cartodb.com/api/v2/sql', params=params)
        print r.status_code
