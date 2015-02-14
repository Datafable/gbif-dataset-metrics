import fileinput

RECORD_ID_INDEX = 0
ISSUE_FIELD_INDEX = 3
DECIMAL_LAT_FIELD_INDEX = 1
DECIMAL_LON_FIELD_INDEX = 2
MAJOR_ISSUES = ['COORDINATE_INVALID', 'COORDINATE_OUT_OF_RANGE', 'ZERO_COORDINATE', 'COUNTRY_COORDINATE_MISMATCH']
MINOR_ISSUES = ['GEODETIC_DATUM_INVALID', 'COORDINATE_REPROJECTION_FAILED', 'COORDINATE_REPROJECTION_SUSPICIOUS']

def get_coordinate_category(issue, decimalLatitude, decimalLongitude):
    issues = issue.strip().split(';')
    for major_issue in MAJOR_ISSUES:
        if major_issue in issues:
            return 'coordinates with major issues'
    for minor_issue in MINOR_ISSUES:
        if minor_issue in issues:
            return 'coordinates with minor issues'
    if decimalLatitude == '' or decimalLatitude == None or decimalLongitude == '' or decimalLongitude == None:
        return 'coordinates not provide'
    return 'valuable coordinates (all in WGS84)'

for line in fileinput.input():
    line = line.split('\t')
    record_id = line[RECORD_ID_INDEX]
    issue = line[ISSUE_FIELD_INDEX].strip()
    decLat = line[DECIMAL_LAT_FIELD_INDEX]
    decLon = line[DECIMAL_LON_FIELD_INDEX]
    coordinate_category = get_coordinate_category(issue, decLat, decLon)
    print ','.join([record_id, decLat, decLon, issue, coordinate_category])
