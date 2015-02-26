import os

ISSUES_TERM = 'http://rs.gbif.org/terms/1.0/issue'


def is_dwca(path):
    return path.lower().endswith('.zip') or os.path.isdir(path)


# Takes a CoreRow and returns a taxon match category, according to:
# https://github.com/peterdesmet/gbif-challenge/issues/39
def get_taxon_match_category(row):
    issues = row.data[ISSUES_TERM]
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


def get_coordinates_quality_category(row):
    issues = row.data[ISSUES_TERM]
    lon = row.data['http://rs.tdwg.org/dwc/terms/decimalLongitude']
    lat = row.data['http://rs.tdwg.org/dwc/terms/decimalLatitude']

    major_issues = ('COORDINATE_INVALID', 'COORDINATE_OUT_OF_RANGE', 'ZERO_COORDINATE',
                    'COUNTRY_COORDINATE_MISMATCH')
    minor_issues = ('GEODETIC_DATUM_INVALID', 'COORDINATE_REPROJECTION_FAILED',
                    'COORDINATE_REPROJECTION_SUSPICIOUS')

    if any(s in issues for s in major_issues):
        return 'COORDINATES_MAJOR_ISSUES'
    elif any(s in issues for s in minor_issues):
        return 'COORDINATES_MINOR_ISSUES'
    elif (len(lat) == 0) or (len(lon) == 0):
        return 'COORDINATES_NOT_PROVIDED'
    else:
        return 'COORDINATES_VALID'


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
