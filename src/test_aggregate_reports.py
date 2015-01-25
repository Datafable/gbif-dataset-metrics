import unittest
import os
import sys
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_PATH + '/src')
import aggregator

class TestAggregator(unittest.TestCase):
    def setUp(self):
        self.agg = aggregator.ReportAggregator()
        self.data_folder = PROJECT_PATH + '/data'

    def test_find_files(self):
        expected_file_names = ['gbif_extract1.report.json', 'gbif_extract2.report.json', 'gbif_extract3.report.json']
        expected_files = [os.path.join(self.data_folder, x) for x in expected_file_names]
        files = self.agg.find_files(self.data_folder)
        self.assertEqual(files, expected_files)

    def test_merge_data(self):
        outdata = {'metric_type1': {'metric1': 10, 'metric2': 2}}
        newdata = {'metric_type1':
                   {'metric1': 2, 'metric2': 5, 'metric3': 1},
                   'metric_type2':
                   {'metric4': 1}
                  }
        mergeddata = {'metric_type1': {'metric1': 12, 'metric2': 7, 'metric3': 1}, 'metric_type2': {'metric4': 1}}
        self.agg.merge_data_set_in_metrics(newdata, outdata)
        self.assertEqual(outdata, mergeddata)

    def test_aggregate_one_dataset(self):
        dataset_key = '3F2504E0-4F89-11D3-9A0C-0305E82C3301'
        human_observations = 3710 + 10134
        unknown = 7 + 9
        fossil_specimen = 3
        machine_observation = 5
        aggregated_metrics = self.agg.aggregate(self.data_folder)
        self.assertEqual(aggregated_metrics[dataset_key]['basisofRecords']['HUMAN_OBSERVATION'], human_observations)
        self.assertEqual(aggregated_metrics[dataset_key]['basisofRecords']['UNKNOWN'], unknown)
        self.assertEqual(aggregated_metrics[dataset_key]['basisofRecords']['FOSSIL_SPECIMEN'], fossil_specimen)
        self.assertEqual(aggregated_metrics[dataset_key]['basisofRecords']['MACHINE_OBSERVATION'], machine_observation)
        self.assertEqual(len(aggregated_metrics.keys()), 3)
