#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to extract dataset metrics from a directory of Darwin Core Archives.

Its output (JSON reports) should then be passed to the aggregation module.
"""

import os
import json
import sys

import argparse

from dwca.read import DwCAReader

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SRC_DIR = os.path.join(CURRENT_DIR, 'src')
sys.path.append(SRC_DIR)

from descriptors import DatasetDescriptor, DatasetDescriptorAwareEncoder  # NOQA
from helpers import (is_dwca, get_taxon_match_category, get_taxonomy,  # NOQA
                     get_coordinates_quality_category, ISSUES_TERM)


# A dot (progress bar) will be printed on screen each time PROGRESS_EACH_X_RECORDS were processed.
PROGRESS_EACH_X_RECORDS = 50000

MULTIMEDIA_ROWTYPE = 'http://rs.gbif.org/terms/1.0/Multimedia'
IDENTIFIER_TERM = 'http://purl.org/dc/terms/identifier'


def parse_archive(a):
    """Parse the archive located at 'a' and return a JSON report."""
    with DwCAReader(a, extensions_to_ignore="verbatim.txt") as dwca:
        r = {}

        # YYYY-MM-DD, polluted with spaces and \n's
        archive_published_at = dwca.metadata.find('dataset').find('pubDate').text.strip()

        i = 0

        for row in dwca:
            # 0. Add dataset if previously unknown...
            dataset_key = row.data['http://rs.gbif.org/terms/1.0/datasetKey']
            if not (dataset_key in r):
                # Newly encountered dataset
                r[dataset_key] = DatasetDescriptor()
                r[dataset_key].set_archive_generated_at(archive_published_at)

            # 1. Increment total number of records per dataset...
            r[dataset_key].increment_number_records()

            bor_term = 'http://rs.tdwg.org/dwc/terms/basisOfRecord'
            r[dataset_key].store_or_increment_bor(row.data[bor_term])
            r[dataset_key].store_or_increment_taxonmatch(get_taxon_match_category(row))
            r[dataset_key].store_or_increment_taxonomy(get_taxonomy(row))

            r[dataset_key].store_or_increment_coordscategory(get_coordinates_quality_category(row))

            # Multimedia categories
            if 'MULTIMEDIA_URL_INVALID' in row.data[ISSUES_TERM]:
                r[dataset_key].mul_increment_invalid_url_count()
            else:
                mul_ext = [m for m in row.extensions if m.rowtype == MULTIMEDIA_ROWTYPE]
                if len(mul_ext) > 0:
                    # Ok, media found
                    r[dataset_key].mul_increment_valid_count()

                    for e in mul_ext:
                        t = e.data['http://purl.org/dc/terms/type']
                        if 'StillImage' in t:
                            r[dataset_key].mul_add_image(row.id, e.data[IDENTIFIER_TERM])
                        elif 'MovingImage' in t:
                            r[dataset_key].mul_add_video(row.id, e.data[IDENTIFIER_TERM])
                        elif 'Audio' in t:
                            r[dataset_key].mul_add_audio(row.id, e.data[IDENTIFIER_TERM])
                        else:
                            r[dataset_key].mul_add_notype(row.id, e.data[IDENTIFIER_TERM])
                else:
                    r[dataset_key].mul_increment_not_provided_count()

            i = i + 1
            if (i % PROGRESS_EACH_X_RECORDS == 0):
                print '.',
                sys.stdout.flush()

        return json.dumps(r, cls=DatasetDescriptorAwareEncoder)


def main():  # NOQA
    d = "Extract dataset metrics from a directory of Darwin Core Archives"

    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('input_dir', help='The input directory containing DwC Archives.')
    parser.add_argument('output_dir', help='The output directory for JSON reports.')
    args = parser.parse_args()

    for entry in os.listdir(args.input_dir):
        entry_w_path = os.path.join(args.input_dir, entry)
        if is_dwca(entry_w_path):
            print "Processing {archive}...".format(archive=entry_w_path)
            report_data = parse_archive(entry_w_path)
            report_filename = entry + '.json'
            report_path = os.path.join(args.output_dir, report_filename)
            print "Done, saving report to {rp}\n".format(rp=report_path)
            r = open(report_path, 'wb')
            r.write(report_data)
            r.close
    print "All archives processed !"

if __name__ == "__main__":
    main()
