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
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 420, 'MEDIA_NOT_PROVIDED': 3293},
                'TAXONOMY': {'taxon1': 10},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 3713
            },
            '05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': {
                'BASISOFRECORDS': { 'UNKNOWN': 6695 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 6595},
                'TAXONOMY': {'taxon1': 13, 'taxon2': 5},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 6695
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'FOSSIL_SPECIMEN': 532, 'UNKNOWN': 10 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 400},
                'TAXONOMY': {'taxon1': 8},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 542
            }
        },
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'HUMAN_OBSERVATION': 10134, 'UNKNOWN': 7 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 400},
                'TAXONOMY': {'taxon2': 30},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 10141
            },
            '05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': {
                'BASISOFRECORDS': { 'UNKNOWN': 89963 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 400},
                'TAXONOMY': {'taxon1': 5},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 89963
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'UNKNOWN': 130 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 400},
                'TAXONOMY': {'taxon1': 10},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 130
            }
        },
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'MACHINE_OBSERVATION': 5, 'UNKNOWN': 9 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 400},
                'TAXONOMY': {'taxon1': 8},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'NUMBER_OF_RECORDS': 14
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'UNKNOWN': 137 },
                'MEDIA_CATEGORIES': {'MEDIA_IMAGE': 10, 'MEDIA_NOT_PROVIDED': 400},
                'TAXONOMY': {'taxon4': 9},
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
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
        media_image = 420 + 10 + 10
        media_not_provided = 3293 + 400 + 400
        taxonomy = {'taxon1': 18, 'taxon2': 30}
        coordinates_not_provided = 3 * 20
        coordinates_minor_issues = 3 * 5
        coordinates_major_issues = 3 * 100
        coordinates_valid = 3 * 200
        aggregated_metrics = self.agg.aggregate(self.test_dir)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['HUMAN_OBSERVATION'], human_observations)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['UNKNOWN'], unknown)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['FOSSIL_SPECIMEN'], fossil_specimen)
        self.assertEqual(aggregated_metrics[dataset_key]['BASISOFRECORDS']['MACHINE_OBSERVATION'], machine_observation)
        self.assertEqual(len(aggregated_metrics.keys()), 3)
        self.assertEqual(aggregated_metrics[dataset_key]['NUMBER_OF_RECORDS'], nr_of_records)
        self.assertEqual(aggregated_metrics[dataset_key]['TAXONOMY']['children'][0]['name'], 'taxon1')
        self.assertEqual(len(aggregated_metrics[dataset_key]['TAXONOMY']['children'][0]['children']), 1)
        self.assertEqual(aggregated_metrics[dataset_key]['TAXONOMY']['children'][1]['name'], 'taxon2')
        self.assertEqual(len(aggregated_metrics[dataset_key]['TAXONOMY']['children'][1]['children']), 1)
        self.assertEqual(aggregated_metrics[dataset_key]['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_NOT_PROVIDED'], coordinates_not_provided)
        self.assertEqual(aggregated_metrics[dataset_key]['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_MINOR_ISSUES'], coordinates_minor_issues)
        self.assertEqual(aggregated_metrics[dataset_key]['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_MAJOR_ISSUES'], coordinates_major_issues)
        self.assertEqual(aggregated_metrics[dataset_key]['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_VALID'], coordinates_valid)
        self.assertEqual(aggregated_metrics[dataset_key]['MEDIA_CATEGORIES']['MEDIA_IMAGE'], media_image)
        self.assertEqual(aggregated_metrics[dataset_key]['MEDIA_CATEGORIES']['MEDIA_NOT_PROVIDED'], media_not_provided)

    def test_get_sum(self):
        test_arrays = [[1, 2, 3], [5, 6, 7]]
        expected_result = 10 # 3 + 7
        result = self.agg._get_sum(test_arrays)
        self.assertEqual(result, expected_result)


    def test_taxonomy_key_to_array(self):
        test1 = 'kingdom1|phylum1|class1|order1|family1|genus1|species1'
        expected1 = ['kingdom1', 'phylum1', 'class1', 'order1', 'family1', 'genus1', 'species1']
        test2 = 'kingdom1|phylum1|class1'
        expected2 = ['kingdom1', 'phylum1', 'class1', 'unknown', 'unknown', 'unknown', 'unknown']
        test3 = 'kingdom1|phylum1|class1||||'
        self.assertEqual(self.agg._taxonkey_to_array(test1), expected1)
        self.assertEqual(self.agg._taxonkey_to_array(test2), expected2)
        self.assertEqual(self.agg._taxonkey_to_array(test3), expected2)

    def test_tree_to_key_value(self):
        intree = {
            'one': {
                'two': {
                    'three': 3,
                    'four': 4
                }
             },
             'five': 5,
             'six': {
                  'seven': 7,
                  'eight': 8
             }
        }
        expected_result = [{
            'name': 'one',
            'children': [{
                'name': 'two',
                'children': [{'name': 'three', 'size': 3}, {'name': 'four', 'size': 4} ]
            }]
        },
        {'name': 'five', 'size': 5 },
        {'name': 'six',
         'children': [{'name': 'seven', 'size': 7}, {'name': 'eight', 'size': 8 } ]
        }
        ]
        result = self.agg._tree_to_dict(intree)
        self.assertEqual(len(result), 3)
        for item in result:
            if item['name'] == 'one':
                self.assertEqual(len(item['children'][0]['children']), 2)
            self.assertTrue(item['name'] in ['one', 'five', 'six'])

    def test_aggregate_taxonomy(self):
        input_taxonomy = {'kingdom1|phylum1|class1|order1|family1|genus1|species1': 10, 'kingdom1|phylum1|class1|order1|family1|genus1|species2': 10}
        expected_result = {
            'name': 'all taxa',
            'children': [
                {
                    'name': 'kingdom1',
                    'children': [{
                        'name:': 'phylum1',
                        'children': [{
                            'name': 'class1',
                            'children': [{
                                'name': 'order1',
                                'children': [{
                                    'name': 'family1',
                                    'children': [{
                                        'name': 'genus1',
                                        'children': [{
                                            'name': 'species1',
                                            'size': 10},
                                        {
                                            'name': 'species2',
                                            'size': 10,
                                        }]
                                    }]
                                }]
                            }]
                        }]
                    }]
                }
            ]
        }

        # aggregate by species
        result = self.agg.aggregate_taxonomy(input_taxonomy, do_genus=True, do_species=True)
        self.assertEqual(result['children'][-1]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['name'], 'species1')
        self.assertEqual(result['children'][-1]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['size'], 10)
        self.assertEqual(result['children'][-1]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['children'][1]['name'], 'species2')
        self.assertEqual(result['children'][-1]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['children'][1]['size'], 10)
        # aggregate by genus
        expected_result = {
            'name': 'all taxa',
            'children': [
                {
                    'name': 'kingdom1',
                    'children': [{
                        'name': 'phylum1',
                        'children': [{
                            'name': 'class1',
                            'children': [{
                                'name': 'order1',
                                'children': [{
                                    'name': 'family1',
                                    'children': [{
                                        'name': 'genus1',
                                        'size': 20
                                    }]
                                }]
                            }]
                        }]
                    }]
                }
            ]
        }
        result = self.agg.aggregate_taxonomy(input_taxonomy, do_genus=True, do_species=False)
        self.assertEqual(result['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['name'], 'genus1')
        self.assertEqual(result['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['size'], 20)
        # aggregate by family
        expected_result = {
            'name': 'all taxa',
            'children': [
                {
                    'name': 'kingdom1',
                    'children': [{
                        'name': 'phylum1',
                        'children': [{
                            'name': 'class1',
                            'children': [{
                                'name': 'order1',
                                'children': [{
                                    'name': 'family1',
                                    'size': 20
                                }]
                            }]
                        }]
                    }]
                }
            ]
        }
        result = self.agg.aggregate_taxonomy(input_taxonomy, do_genus=False, do_species=False)
        self.assertEqual(result['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['name'], 'family1')
        self.assertEqual(result['children'][0]['children'][0]['children'][0]['children'][0]['children'][0]['size'], 20)
