import unittest
import os
import pickle
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
                'TAXONOMY': {'taxon1': 10},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'audio': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'stillimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'no_type': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'media_not_provided': 37,
                    'media_url_invalid': 12,
                    'media_valid': 61,
                },
                'NUMBER_OF_RECORDS': 3713
            },
            '05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': {
                'BASISOFRECORDS': { 'UNKNOWN': 6695 },
                'TAXONOMY': {'taxon1': 13, 'taxon2': 5},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'audio': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'stillimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'no_type': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'media_not_provided': 37,
                    'media_url_invalid': 12,
                    'media_valid': 61,
                },
                'NUMBER_OF_RECORDS': 6695
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'FOSSIL_SPECIMEN': 532, 'UNKNOWN': 10 },
                'TAXONOMY': {'taxon1': 8},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'audio': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'stillimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'no_type': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'media_not_provided': 37,
                    'media_url_invalid': 12,
                    'media_valid': 61,
                },
                'NUMBER_OF_RECORDS': 542
            }
        },
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'HUMAN_OBSERVATION': 10134, 'UNKNOWN': 7 },
                'TAXONOMY': {'taxon2': 30},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid3': ['url4', 'url5'],
                        'occid4': ['url6']
                    },
                    'audio': {
                        'occid3': ['url4', 'url5'],
                        'occid4': ['url6']
                    },
                    'stillimage': {
                        'occid3': ['url4', 'url5'],
                        'occid4': ['url6']
                    },
                    'no_type': {
                        'occid3': ['url4', 'url5'],
                        'occid4': ['url6']
                    },
                    'media_not_provided': 15,
                    'media_url_invalid': 2,
                    'media_valid': 20,
                },
                'NUMBER_OF_RECORDS': 10141
            },
            '05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': {
                'BASISOFRECORDS': { 'UNKNOWN': 89963 },
                'TAXONOMY': {'taxon1': 5},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'audio': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'stillimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'no_type': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'media_not_provided': 37,
                    'media_url_invalid': 12,
                    'media_valid': 61,
                },
                'NUMBER_OF_RECORDS': 89963
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'UNKNOWN': 130 },
                'TAXONOMY': {'taxon1': 10},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'audio': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'stillimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'no_type': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'media_not_provided': 37,
                    'media_url_invalid': 12,
                    'media_valid': 61,
                },
                'NUMBER_OF_RECORDS': 130
            }
        },
        {
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': {
                'BASISOFRECORDS': { 'MACHINE_OBSERVATION': 5, 'UNKNOWN': 9 },
                'TAXONOMY': {'taxon1': 8},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {},
                    'audio': {},
                    'stillimage': {},
                    'no_type': {},
                    'media_not_provided': 10,
                    'media_url_invalid': 10,
                    'media_valid': 10,
                },
                'NUMBER_OF_RECORDS': 14
            },
            '82746a3e-f762-11e1-a439-00145eb45e9a': {
                'BASISOFRECORDS': { 'UNKNOWN': 137 },
                'TAXONOMY': {'taxon4': 9},
                'TAXON_MATCHES': {
                    'TAXON_MATCH_HIGHERRANK': 10,
                    'TAXON_MATCH_FUZZY': 10,
                    'TAXON_MATCH_COMPLETE': 10,
                    'TAXON_NOT_PROVIDED': 10 
                },
                'COORDINATE_QUALITY_CATEGORIES': {
                    'COORDINATES_NOT_PROVIDED': 20,
                    'COORDINATES_MINOR_ISSUES': 5,
                    'COORDINATES_MAJOR_ISSUES': 100,
                    'COORDINATES_VALID': 200
                },
                'MEDIA': {
                    'movingimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'audio': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'stillimage': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'no_type': {
                        'occid1': ['url1', 'url2'],
                        'occid2': ['url3']
                    },
                    'media_not_provided': 37,
                    'media_url_invalid': 12,
                    'media_valid': 61,
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
        self.agg_man = aggregator.AggregationJobsManager()
        self.createFixtureData()

    def tearDown(self):
        for f in self.test_files:
            os.remove(f)

    @unittest.SkipTest
    def test_find_files(self):
        files = self.agg.find_files(self.test_dir)
        self.assertEqual(files, self.test_files)

    def compare_indices(self, index, expected_index):
        for dataset, files in expected_index.iteritems():
            full_paths_array = []
            for f in files:
                f = os.path.join(self.test_dir, f)
                full_paths_array.append(f)
            self.assertEqual(index[dataset], full_paths_array)

    def test_create_index(self):
        expected_index = {'05ebc824-3a3b-4f64-ab22-99b0e2c3aa48': ['gbif_extract0.json', 'gbif_extract1.json'],
            '3F2504E0-4F89-11D3-9A0C-0305E82C3301': ['gbif_extract0.json', 'gbif_extract1.json', 'gbif_extract2.json'],
            '82746a3e-f762-11e1-a439-00145eb45e9a': ['gbif_extract0.json', 'gbif_extract1.json', 'gbif_extract2.json']}
        index = self.agg_man.createIndex(self.test_dir)
        self.compare_indices(index, expected_index)
        indexfile = open(os.path.join(self.test_dir, 'dataset_index.pkl'))
        written_index = pickle.load(indexfile)
        self.compare_indices(written_index, expected_index)

    def test_aggregate_one_dataset(self):
        dataset_key = '3F2504E0-4F89-11D3-9A0C-0305E82C3301'
        human_observations = 3710 + 10134
        unknown = 7 + 9
        fossil_specimen = 3
        machine_observation = 5
        nr_of_records = 3710 + 10134 + 7 + 9 + 3 + 5
        taxonomy = {'taxon1': 18, 'taxon2': 30}
        coordinates_not_provided = 3 * 20
        coordinates_minor_issues = 3 * 5
        coordinates_major_issues = 3 * 100
        coordinates_valid = 3 * 200
        taxon_higher_rank = 3 * 10
        taxon_fuzzy = 3 * 10
        taxon_complete = 3 * 10
        taxon_not_provided = 3 * 10
        media_not_provided = 37 + 15 + 10
        media_url_invalid = 12 + 2 + 10
        media_valid = 61 + 20 + 10
        movingimage = {u'occid1': [u'url1', u'url2'], u'occid3': [u'url4', u'url5'], u'occid2': [u'url3'], u'occid4': [u'url6']}
        stillimage = movingimage
        audio = movingimage
        notype = movingimage
        aggregated_metrics = self.agg.aggregate_dataset({'index': [dataset_key, self.test_files], 'api_key': None})
        self.assertEqual(aggregated_metrics['BASISOFRECORDS']['HUMAN_OBSERVATION'], human_observations)
        self.assertEqual(aggregated_metrics['BASISOFRECORDS']['UNKNOWN'], unknown)
        self.assertEqual(aggregated_metrics['BASISOFRECORDS']['FOSSIL_SPECIMEN'], fossil_specimen)
        self.assertEqual(aggregated_metrics['BASISOFRECORDS']['MACHINE_OBSERVATION'], machine_observation)
        self.assertEqual(aggregated_metrics['NUMBER_OF_RECORDS'], nr_of_records)
        self.assertEqual(aggregated_metrics['TAXONOMY']['children'][0]['name'], 'taxon1')
        self.assertEqual(len(aggregated_metrics['TAXONOMY']['children'][0]['children']), 1)
        self.assertEqual(aggregated_metrics['TAXONOMY']['children'][1]['name'], 'taxon2')
        self.assertEqual(len(aggregated_metrics['TAXONOMY']['children'][1]['children']), 1)
        self.assertEqual(aggregated_metrics['TAXON_MATCHES']['TAXON_MATCH_HIGHERRANK'], taxon_higher_rank)
        self.assertEqual(aggregated_metrics['TAXON_MATCHES']['TAXON_MATCH_FUZZY'], taxon_fuzzy)
        self.assertEqual(aggregated_metrics['TAXON_MATCHES']['TAXON_MATCH_COMPLETE'], taxon_complete)
        self.assertEqual(aggregated_metrics['TAXON_MATCHES']['TAXON_NOT_PROVIDED'], taxon_not_provided)
        self.assertEqual(aggregated_metrics['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_NOT_PROVIDED'], coordinates_not_provided)
        self.assertEqual(aggregated_metrics['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_MINOR_ISSUES'], coordinates_minor_issues)
        self.assertEqual(aggregated_metrics['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_MAJOR_ISSUES'], coordinates_major_issues)
        self.assertEqual(aggregated_metrics['COORDINATE_QUALITY_CATEGORIES']['COORDINATES_VALID'], coordinates_valid)
        self.assertEqual(aggregated_metrics['MEDIA']['media_not_provided'], media_not_provided)
        self.assertEqual(aggregated_metrics['MEDIA']['media_url_invalid'], media_url_invalid)
        self.assertEqual(aggregated_metrics['MEDIA']['media_valid'], media_valid)
        for mediatypes in [['movingimage', movingimage], ['stillimage', stillimage], ['audio', audio], ['no_type', notype]]:
            mediatype_key, expected = mediatypes
            result = aggregated_metrics['MEDIA'][mediatype_key]
            keys_result = result.keys()
            keys_result.sort()
            occid1_result = result['occid1']
            occid1_result.sort()
            occid2_result = result['occid2']
            occid2_result.sort()
            keys_expected = expected.keys()
            keys_expected.sort()
            occid1_expected = expected['occid1']
            occid1_expected.sort()
            occid2_expected = expected['occid2']
            occid2_expected.sort()
            # assert that the keys (occurrence ids) are as expected
            self.assertEqual(keys_result, keys_expected)
            # assert that the values (media urls) are as expected for 2 occurrences
            self.assertEqual(occid1_result, occid1_expected)
            self.assertEqual(occid2_result, occid2_expected)

    def test_get_images_sample(self):
        data = {'stillimage': {'occ1': [], 'occ2': [], 'occ3': [], 'occ4': []}}
        counter = 1
        for occ in data['stillimage'].keys():
            for i in range(5):
                data['stillimage'][occ].append('url' + str(counter))
                counter += 1
        result = self.agg.get_images_sample(data, 2)
        self.assertEqual(len(result.keys()), 2)

    def test_get_sum(self):
        test_arrays = [[1, 2, 3], [5, 6, 7]]
        expected_result = 10 # 3 + 7
        result = self.agg._get_sum(test_arrays)
        self.assertEqual(result, expected_result)


    def test_taxonomy_key_to_array(self):
        test1 = 'kingdom1|phylum1|class1|order1|family1|genus1|species1'
        expected1 = ['kingdom1', 'phylum1', 'class1', 'order1', 'family1', 'genus1', 'species1']
        test2 = 'kingdom1|phylum1|class1'
        expected2 = ['kingdom1', 'phylum1', 'class1', 'Unknown', 'Unknown', 'Unknown', 'Unknown']
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
            'name': 'All taxa',
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
            'name': 'All taxa',
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
            'name': 'All taxa',
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
