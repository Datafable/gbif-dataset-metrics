#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Pep8
# TODO: Add Belgian Coccinellidae - Ladybird bee… to test data
# TODO: Ensure it works with multuiple dataset per archive
# TODO: output: unicode string or not ?
import os
import json

from dwca.read import DwCAReader

# A report file will be generated for each DwC-A in this directory.
# All zip files and subdirectories will be assumed to be DwC-A
DATA_SOURCE_DIR = os.path.join(os.path.dirname(__file__), 'sample_base_data')
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')


class DatasetDescriptorAwareEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DatasetDescriptor):
            return str(obj.data)

        return json.JSONEncoder.default(self, obj)


class DatasetDescriptor(object):
    def __init__(self):
        self.data = {'NUMBER_OF_RECORDS': 0, 
                     'BASISOFRECORDS': {}}

    def increment_number_records(self):
        self.data['NUMBER_OF_RECORDS'] = self.data['NUMBER_OF_RECORDS'] + 1

    def store_or_increment_bor(self, value):
        if value in self.data['BASISOFRECORDS']:
            self.data['BASISOFRECORDS'][value] = self.data['BASISOFRECORDS'][value] + 1
        else:
            self.data['BASISOFRECORDS'][value] = 1


# Parse the archive located at 'a' and return a JSON report
def parse_archive(a):
    with DwCAReader(a) as dwca:
        r = {}

        for row in dwca:
            # 0. Add dataset if previously unknown...
            dataset_key = row.data['http://rs.gbif.org/terms/1.0/datasetKey']
            if not (dataset_key in r):
                # Newly encountered dataset
                r[dataset_key] = DatasetDescriptor()

            # 1. Increment total number of records per dataset...
            r[dataset_key].increment_number_records()
            r[dataset_key].store_or_increment_bor(row.data['http://rs.tdwg.org/dwc/terms/basisOfRecord'])

        return json.dumps(r, cls=DatasetDescriptorAwareEncoder)


def is_dwca(path):
    return path.lower().endswith('.zip') or os.path.isdir(path)

def main():
    for entry in os.listdir(DATA_SOURCE_DIR):
        entry_w_path = os.path.join(DATA_SOURCE_DIR, entry)
        if is_dwca(entry_w_path):
            print "Processing {archive}...".format(archive=entry_w_path)
            report_data = parse_archive(entry_w_path)
            report_filename = entry + '.json'
            report_path = os.path.join(REPORTS_DIR, report_filename)
            print "Done, saving report to {rp}".format(rp=report_path)
            r = open(report_path, 'wb')
            r.write(report_data)
            r.close
    print "All archives processed !"

if __name__ == "__main__":
    main()