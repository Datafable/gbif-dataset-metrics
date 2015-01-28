import os


def is_dwca(path):
    return path.lower().endswith('.zip') or os.path.isdir(path)


# Takes a CoreRow and returns a taxon match category, according to:
# https://github.com/peterdesmet/gbif-challenge/issues/39
def get_taxon_match_category(row):
    issues = row.data['http://rs.gbif.org/terms/1.0/issue']
    genus = row.data['http://rs.tdwg.org/dwc/terms/genus']
    scientific_name = row.data['http://rs.tdwg.org/dwc/terms/scientificName']

    if (len(scientific_name) == 0 or len(genus) == 0):
        return 'TAXON_NOT_PROVIDED'
    elif 'TAXON_MATCH_NONE' in issues:
        return 'TAXON_MATCH_NONE'
    elif 'TAXON_MATCH_HIGHERRANK' in issues:
        return 'TAXON_MATCH_HIGHERRANK'
    elif 'TAXON_MATCH_FUZZY' in issues:
        return 'TAXON_MATCH_FUZZY'
    else:
        return 'TAXON_MATCH_COMPLETE'
