from glob import glob
import json

class ReportAggregator():
    def find_files(self, folder):
        files = glob(folder + '/gbif_extract*.report.json')
        return files

    def merge_data_set_in_metrics(self, dataset, metrics_data):
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
