#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys

from dwca.read import DwCAReader

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SRC_DIR = os.path.join(CURRENT_DIR, 'src')
sys.path.append(SRC_DIR)

from descriptors import DatasetDescriptor, DatasetDescriptorAwareEncoder
from helpers import (is_dwca, get_taxon_match_category, get_taxonomy,
                     get_coordinates_quality_category, ISSUES_TERM)

# A report file will be generated for each DwC-A in this directory.
# All zip files and subdirectories will be assumed to be DwC-A
DATA_SOURCE_DIR = os.path.join(CURRENT_DIR, 'sample_base_data')
REPORTS_DIR = os.path.join(CURRENT_DIR, 'reports')

# A dot (progress bar) will be printed on screen each time PROGRESS_EACH_X_RECORDS were processed.
PROGRESS_EACH_X_RECORDS = 1000


# Parse the archive located at 'a' and return a JSON report
def parse_archive(a):
    with DwCAReader(a, extensions_to_ignore="verbatim.txt") as dwca:
        r = {}

        i = 0
        for row in dwca:
            # 0. Add dataset if previously unknown...
            dataset_key = row.data['http://rs.gbif.org/terms/1.0/datasetKey']
            if not (dataset_key in r):
                # Newly encountered dataset
                r[dataset_key] = DatasetDescriptor()

            # 1. Increment total number of records per dataset...
            r[dataset_key].increment_number_records()

            bor_term = 'http://rs.tdwg.org/dwc/terms/basisOfRecord'
            r[dataset_key].store_or_increment_bor(row.data[bor_term])
            r[dataset_key].store_or_increment_taxonmatch(get_taxon_match_category(row))
            r[dataset_key].store_or_increment_taxonomy(get_taxonomy(row))

            r[dataset_key].store_or_increment_coordinatecategory(get_coordinates_quality_category(row))

            if 'MULTIMEDIA_URL_INVALID' in row.data[ISSUES_TERM]:
                r[dataset_key].mul_increment_invalid_url_count()
            else:
                mul_ext = [m for m in row.extensions if m.rowtype == 'http://rs.gbif.org/terms/1.0/Multimedia']
                if len(mul_ext) > 0:
                    # Ok, media found
                    r[dataset_key].mul_increment_valid_count()

                    for e in mul_ext:
                        t = e.data['http://purl.org/dc/terms/type']
                        if 'StillImage' in t:
                            r[dataset_key].mul_add_image(row.id, e.data['http://purl.org/dc/terms/references'])
                        elif 'MovingImage' in t:
                            r[dataset_key].mul_add_video(row.id, e.data['http://purl.org/dc/terms/references'])
                        elif 'Audio' in t:
                            r[dataset_key].mul_add_audio(row.id, e.data['http://purl.org/dc/terms/references'])
                        else:
                            r[dataset_key].mul_add_notype(row.id, e.data['http://purl.org/dc/terms/references'])
                else:
                    r[dataset_key].mul_increment_not_provided_count()

            i = i + 1
            if (i % PROGRESS_EACH_X_RECORDS == 0):
                print '.',
                sys.stdout.flush()

        return json.dumps(r, cls=DatasetDescriptorAwareEncoder)


def main():
    for entry in os.listdir(DATA_SOURCE_DIR):
        entry_w_path = os.path.join(DATA_SOURCE_DIR, entry)
        if is_dwca(entry_w_path):
            print "Processing {archive}...".format(archive=entry_w_path)
            report_data = parse_archive(entry_w_path)
            report_filename = entry + '.json'
            report_path = os.path.join(REPORTS_DIR, report_filename)
            print "Done, saving report to {rp}\n".format(rp=report_path)
            r = open(report_path, 'wb')
            r.write(report_data)
            r.close
    print "All archives processed !"

if __name__ == "__main__":
    main()
