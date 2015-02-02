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
    for dataset in data:
        row = []
        basis_of_records = data[dataset]['BASISOFRECORDS']
        for metric_name in basis_of_records_metrics:
            if metric_name in basis_of_records:
                row.append(basis_of_records[metric_name])
            else:
                row.append(0)
        nr_of_records = data[dataset]['NUMBER_OF_RECORDS']
        row.append(nr_of_records)
        row.append(dataset)
        writer.write_basis_of_record(row, settings['api_key'])

def main():
    data_dir, settings_file = check_arguments()
    data = aggregate_metrics(data_dir)
    write_data(data, settings_file)

main()
