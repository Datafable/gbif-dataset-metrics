import sys
import json
import os
import requests
src_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/src'
sys.path.append(src_path)
from aggregator import CartoDBWriter, ReportAggregator



def check_arguments():
    if len(sys.argv) is not 3:
        print 'usage: ./merge_taxonomy.py <taxonomy file> <settings file>'
        sys.exit(-1)
    return sys.argv[1:]

def parse_taxonomy_line(inline):
    inline = inline.lstrip()
    first_space_index = inline.find(' ')
    count = inline[0:first_space_index]
    taxonomy_line = inline[first_space_index+1:]
    values = taxonomy_line.split('\t')
    values[-1] = values[-1].strip()
    values = [x if x is not '' else 'undetermined' for x in values]
    values.append(count)
    return values

def main():
    infile, settingsfile = check_arguments()
    agg = ReportAggregator()
    writer = CartoDBWriter()
    settings = json.load(open(settingsfile))
    api_key = settings['api_key']
    inlines = open(infile).readlines()
    taxonomy_lines = [parse_taxonomy_line(x) for x in inlines]
    if len(taxonomy_lines) < 1000:
        taxonomy_tree = agg.aggregate_taxonomy(taxonomy_lines, do_genus=True, do_species=True)
    elif len(taxonomy_lines) < 10000:
        taxonomy_tree = agg.aggregate_taxonomy(taxonomy_lines, do_genus=True, do_species=False)
    else:
        taxonomy_tree = agg.aggregate_taxonomy(taxonomy_lines, do_genus=False, do_species=False)
    for dataset in taxonomy_tree:
        tree = taxonomy_tree[dataset]
        writer.writeTaxonomy(dataset, json.dumps(tree), api_key)

main()
