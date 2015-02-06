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


# Takes a CoreRow and returns a media type category, according to:
# https://github.com/peterdesmet/gbif-challenge/issues/43
def get_media_type_category(row):
    issues = row.data['http://rs.gbif.org/terms/1.0/issue']
    media_types = row.data['http://rs.gbif.org/terms/1.0/mediaType']

    if 'MULTIMEDIA_URI_INVALID' in issues:
        return 'MEDIA_URL_INVALID'
    elif 'MOVINGIMAGE' in media_types:
        return 'MEDIA_VIDEO'
    elif 'AUDIO' in media_types:
        return 'MEDIA_AUDIO'
    elif 'STILLIMAGE' in media_types:
        return 'MEDIA_IMAGE'
    else:
        return 'MEDIA_NOT_PROVIDED'


def get_taxonomy(row):
    """ Takes a CoreRow, and returns taxonomy such as:
    'kingdom1|phylum1|class1|order1|family1|genus1|species1'.

    Missing fields can stay blank: 'kingdom1|phylum1|class1||||'.
    """

    kingdom = row.data['http://rs.tdwg.org/dwc/terms/kingdom'].strip()
    phylum = row.data['http://rs.tdwg.org/dwc/terms/phylum'].strip()
    class_ = row.data['http://rs.tdwg.org/dwc/terms/class'].strip()
    order = row.data['http://rs.tdwg.org/dwc/terms/order'].strip()
    family = row.data['http://rs.tdwg.org/dwc/terms/family'].strip()
    genus = row.data['http://rs.tdwg.org/dwc/terms/genus'].strip()
    species = row.data['http://rs.tdwg.org/dwc/terms/specificEpithet'].strip()

    return u"{k}|{p}|{c}|{o}|{f}|{g}|{s}".format(k=kingdom, p=phylum, c=class_,
                                                 o=order, f=family, g=genus, s=species)
