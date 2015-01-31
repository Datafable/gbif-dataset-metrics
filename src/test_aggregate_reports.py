import unittest
import os
import sys
import json
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_PATH + '/src')
import aggregator

class TestAggregator(unittest.TestCase):
    def createFixtureData(self):
        data = [
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'HUMAN_OBSERVATION': 3710, 'FOSSIL_SPECIMEN': 3 },
                'NUMBER_OF_RECORDS': 3713
            },
            '05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': {
                'BASISOFRECORDS': { 'UNKNOWN': 6695 },
                'NUMBER_OF_RECORDS': 6695
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'FOSSIL_SPECIMEN': 532, 'UNKNOWN': 10 },
                'NUMBER_OF_RECORDS': 542
            }
        },
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'HUMAN_OBSERVATION': 10134, 'UNKNOWN': 7 },
                'NUMBER_OF_RECORDS': 10141
            },
            '05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': {
                'BASISOFRECORDS': { 'UNKNOWN': 89963 },
                'NUMBER_OF_RECORDS': 89963
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'UNKNOWN': 130 },
                'NUMBER_OF_RECORDS': 130
            }
        },
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'MACHINE_OBSERVATION': 5, 'UNKNOWN': 9 },
                'NUMBER_OF_RECORDS': 14
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'UNKNOWN': 137 },
                'NUMBER_OF_RECORDS': 137
            }
        }
        ]
        self.test_dir = os.path.join(PROJECT_PATH, 'data')
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        for index, data_blob in enumerate(data):
            file_name = os.path.join(self.test_dir, 'gbif_extract{0}.json'.format(index))
            self.test_files.append(file_name)
            f = open(file_name, 'wb')
            f.write(json.dumps(data_blob))
            f.close()

    def setUp(self):
        self.test_files = []
        self.agg = aggregator.ReportAggregator()
        self.createFixtureData()

    def tearDown(self):
        for f in self.test_files:
            os.remove(f)

    @unittest.SkipTest
    def test_find_files(self):
        files = self.agg.find_files(self.test_dir)
        self.assertEqual(files, self.test_files)

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
        nr_of_records = 3710 + 10134 + 7 + 9 + 3 + 5
        aggregated_metrics = self.agg.aggregate(self.test_dir)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['HUMAN_OBSERVATION'], human_observations)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['UNKNOWN'], unknown)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['FOSSIL_SPECIMEN'], fossil_specimen)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['MACHINE_OBSERVATION'], machine_observation)
        self.assertEqual(len(aggregated_metrics.keys()), 3)
        self.assertEqual(aggregated_metrics[dataset_key]['NUMBER_OF_RECORDS'], nr_of_records)

    def test_get_sum(self):
        test_arrays = [[1, 2, 3], [5, 6, 7]]
        expected_result = 10 # 3 + 7
        result = self.agg._get_sum(test_arrays)
        self.assertEqual(result, expected_result)

    def test_aggregate_taxonomy(self):
        record1 = ['dataset1', 'kingdom1', 'phylum1', 'class1', 'order1', 'family1', 'genus1', 'species1', 10]
        record2 = ['dataset1', 'kingdom1', 'phylum1', 'class1', 'order1', 'family1', 'genus1', 'species2', 10]
        expected_result = {
            'dataset1': {
                'kingdom1': {
                    'phylum1': {
                        'class1': {
                            'order1': {
                                'family1': {
                                    'genus1': {
                                        'species1': 10,
                                        'species2': 10,
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        # aggregate by species
        result = self.agg.aggregate_taxonomy([record1, record2], do_genus=True, do_species=True)
        self.assertEqual(json.dumps(result), json.dumps(expected_result))
        # aggregate by genus
        expected_result = {
            'dataset1': {
                'kingdom1': {
                    'phylum1': {
                        'class1': {
                            'order1': {
                                'family1': {
                                    'genus1': 20
                                }
                            }
                        }
                    }
                }
            }
        }
        result = self.agg.aggregate_taxonomy([record1, record2], do_genus=True, do_species=False)
        self.assertEqual(json.dumps(result), json.dumps(expected_result))
        # aggregate by family
        expected_result = {
            'dataset1': {
                'kingdom1': {
                    'phylum1': {
                        'class1': {
                            'order1': {
                                'family1': 20
                            }
                        }
                    }
                }
            }
        }
        result = self.agg.aggregate_taxonomy([record1, record2], do_genus=False, do_species=False)
        self.assertEqual(json.dumps(result), json.dumps(expected_result))
