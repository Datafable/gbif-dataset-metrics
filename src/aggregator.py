from glob import glob
import json
import os
import requests

class ReportAggregator():
    """
    This class will be used to aggregate gbif_extract*.report.json files.
    Metric data will be aggregated by data set key
    """

    def find_files(self, folder):
        """
        Look for all gbif_extract*.report.json files
        in a given folder.
        """
        files = glob(folder + '/gbif_extract*.report.json')
        return files

    def merge_data_set_in_metrics(self, dataset, metrics_data):
        """
        merge the metric data by metric type and metric name
        """
        for metric_type in dataset.keys():
            if metric_type in metrics_data.keys():
                for metric_name in dataset[metric_type].keys():
                    if metric_name in metrics_data[metric_type].keys():
                        metrics_data[metric_type][metric_name] += dataset[metric_type][metric_name]
                    else:
                        metrics_data[metric_type][metric_name] = dataset[metric_type][metric_name]
            else:
                metrics_data[metric_type] = dataset[metric_type]
        return True
                

    def aggregate(self, data_folder):
        """
        iterate over all the gbif_extract*.report.json files
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

class CartoDBWriter():
    def __init__(self):
        PRJ_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.sql_statement = "delete from gbif_dataset_metrics where dataset_key='{0}'; insert into gbif_dataset_metrics (dataset_key, bor_preserved_specimen, bor_fossil_specimen, bor_living_specimen, bor_material_sample, bor_observation, bor_human_observation, bor_machine_observation, bor_literature, bor_unknown, occurrences) values ('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})"
        self.settings = json.load(open(PRJ_DIR + '/settings.json'))

    def write_basis_of_record(self, row):
        params = {'q': self.sql_statement.format(*row), 'api_key': self.settings['api_key']}
        requests.get('http://datafable.cartodb.com/api/v2/sql', params=params)
