from glob import glob
import json
import requests

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

class CartoDBWriter():
    def __init__(self):
        self.sql_statement = "update gbif_dataset_metrics set bor_preserved_specimen={0}, bor_fossil_specimen={1}, bor_living_specimen={2}, bor_material_sample={3}, bor_observation={4}, bor_human_observation={5}, bor_machine_observation={6}, bor_literature={7}, bor_unknown={8}, occurrences={9} where dataset_key='{10}'"

    def write_basis_of_record(self, row, api_key):
        params = {'q': self.sql_statement.format(*row), 'api_key': api_key}
        requests.get('http://datafable.cartodb.com/api/v2/sql', params=params)
