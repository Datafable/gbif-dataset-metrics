import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from aggregator import  CartoDBWriter
import json
from operator import itemgetter
from itertools import groupby

def parse_line(inline):
    line = inline.lstrip()
    first_space_index = line.find(' ')
    count = line[0:first_space_index]
    taxonomy_line = line[first_space_index + 1:]
    taxonomy = taxonomy_line.split('\t')
    taxonomy[-1] = taxonomy[-1].strip()
    taxonomy.append(count)
    return taxonomy

def merge_by_species(inlines, do_species=True):
    tree = {}
    total = 0
    for arr in inlines:
        species = arr[7]
        if species == '':
            species = 'undetermined'
        count = arr[8]
        if do_species:
            tree[species] = int(count)
        else:
            total += int(count)
    if do_species:
        return tree
    else:
        return total

def merge_by_genus(inlines, do_species=True, do_genus=True):
    tree = {}
    total = 0
    for genus, lines in groupby(inlines, itemgetter(6)):
        if genus == '':
            genus = 'undetermined'
        taxonomy_for_this_genus = merge_by_species(lines, do_species=do_species)
        if do_genus:
            tree[genus] = taxonomy_for_this_genus
        else:
            total += taxonomy_for_this_genus
    if do_genus:
        return tree
    else:
        return total

def merge_by_family(inlines, do_species=True, do_genus=True):
    tree = {}
    for family, lines in groupby(inlines, itemgetter(5)):
        if family == '':
            family = 'undetermined'
        taxonomy_for_this_family = merge_by_genus(lines, do_species=do_species, do_genus=do_genus)
        tree[family] = taxonomy_for_this_family
    return tree

def merge_by_order(inlines, do_species=True, do_genus=True):
    tree = {}
    for order, lines in groupby(inlines, itemgetter(4)):
        if order == '':
            order = 'undetermined'
        taxonomy_for_this_order = merge_by_family(lines, do_species=do_species, do_genus=do_genus)
        tree[order] = taxonomy_for_this_order
    return tree

def merge_by_class(inlines, do_species=True, do_genus=True):
    tree = {}
    for clss, lines in groupby(inlines, itemgetter(3)):
        if clss == '':
            clss = 'undetermined'
        taxonomy_for_this_class = merge_by_order(lines, do_species=do_species, do_genus=do_genus)
        tree[clss] = taxonomy_for_this_class
    return tree

def merge_by_phylum(inlines, do_species=True, do_genus=True):
    tree = {}
    for phylum, lines in groupby(inlines, itemgetter(2)):
        if phylum == '':
            phylum = 'undetermined'
        taxonomy_for_this_phylum = merge_by_class(lines, do_species=do_species, do_genus=do_genus)
        tree[phylum] = taxonomy_for_this_phylum
    return tree

def merge_by_kingdom(inlines, do_species=True, do_genus=True):
    tree = {}
    for kingdom, lines in groupby(inlines, itemgetter(1)):
        if kingdom == '':
            kingdom = 'undetermined'
        taxonomy_for_this_kingdom = merge_by_phylum(lines, do_species=do_species, do_genus=do_genus)
        tree[kingdom] = taxonomy_for_this_kingdom
    return tree

def merge_by_dataset(inlines, api_key, do_species=True, do_genus=True):
    writer = CartoDBWriter()
    for dataset_key, lines in groupby(inlines, itemgetter(0)):
        if dataset_key is not '':
            taxonomy_for_this_dataset = merge_by_kingdom(lines, do_species=do_species, do_genus=do_genus)
            #writer.writeTaxonomy(dataset_key, json.dumps(taxonomy_for_this_dataset), api_key)
            writer.writeTaxonomy(dataset_key, 'test', api_key)

def check_arguments():
    if len(sys.argv) != 3:
        print 'usage: merge_taxonomy_2icicle.py <infile> <settings file>'
        sys.exit(-1)
    return sys.argv[1:]

def main():
    infile, settings_file = check_arguments()
    settings = json.load(open(settings_file))
    api_key = settings['api_key']
    f = open(infile)
    lines = f.readlines()
    nr_of_taxa = len(lines)
    taxonomy_lines = [parse_line(x) for x in lines]
    if nr_of_taxa < 1000:
        merge_by_dataset(taxonomy_lines, api_key, do_species=True, do_genus=True)
    elif nr_of_taxa < 10000:
        merge_by_dataset(taxonomy_lines, api_key, do_species=False, do_genus=True)
    else:
        merge_by_dataset(taxonomy_lines, api_key, do_species=False, do_genus=False)

main()
