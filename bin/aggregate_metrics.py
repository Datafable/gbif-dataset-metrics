import sys
import os
import json
SRC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/src'
sys.path.append(SRC_DIR)
from aggregator import ReportAggregator, CartoDBWriter

def check_arguments():
    if len(sys.argv) != 3:
        print 'usage: aggregate_metrics.py <data directory> <settings.json>\n'
        print '    data directory:  this should point to a directory'
        print '                     containing chunks of metric data.'
        print '                     metric data should be in json and'
        print '                     ordered by dataset key.\n'
        print '    settings.json:   contains the `api_key` that will'
        print '                     be used to contact the cartodb API.'
        sys.exit(-1)
    data_dir, settings_file = sys.argv[1:]
    return [data_dir, settings_file]

def aggregate_metrics(data_dir):
    agg = ReportAggregator()
    data = agg.aggregate(data_dir)
    return data

def write_data(data, settings_file):
    settings = json.load(open(settings_file))
    writer = CartoDBWriter()
    basis_of_records_metrics = ['PRESERVED_SPECIMEN', 'FOSSIL_SPECIMEN', 'LIVING_SPECIMEN', 'MATERIAL_SAMPLE', 'OBSERVATION', 'HUMAN_OBSERVATION', 'MACHINE_OBSERVATION', 'LITERATURE', 'UNKNOWN']
    taxon_match_metrics = ['TAXON_NOT_PROVIDED', 'TAXON_MATCH_NONE', 'TAXON_MATCH_HIGHERRANK', 'TAXON_MATCH_FUZZY', 'TAXON_MATCH_COMPLETE']
    for dataset in data:
        basis_of_records = data[dataset]['BASISOFRECORDS']
        taxon_match = data[dataset]['TAXON_MATCHES']
        basis_of_record_data = [basis_of_records[x] if x in basis_of_records.keys() else 0 for x in basis_of_records_metrics]
        taxon_match_data = [taxon_match[x] if x in taxon_match.keys() else 0 for x in taxon_match_metrics]
        nr_of_records = data[dataset]['NUMBER_OF_RECORDS']
        taxonomy = json.dumps(data[dataset]['TAXONOMY'])
        row = basis_of_record_data + taxon_match_data + [nr_of_records, taxonomy, dataset]
        writer.write_metrics(row, settings['api_key'])

def main():
    data_dir, settings_file = check_arguments()
    data = aggregate_metrics(data_dir)
    write_data(data, settings_file)

main()