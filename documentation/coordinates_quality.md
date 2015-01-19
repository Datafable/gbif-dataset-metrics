# Coordinates quality

## Description

For each occurrence we assess the quality of the provided coordinates. 

## Suggestions for GBIF

* `hasCoordinate` is always `false` in the download files. It is provided correctly via the API. This seems like a bug.
* Provide more specific documentation regarding [hasCoordinate](http://gbif.github.io/dwc-api/apidocs/org/gbif/dwc/terms/GbifTerm.html#hasCoordinate): what is a valid latitude/longitude. What coordinate issues (e.g. `ZERO_COORDINATE`) make the coordinates invalid?
* Provice more specific documentation regarding [hasGeospatialIssues](http://gbif.github.io/dwc-api/apidocs/org/gbif/dwc/terms/GbifTerm.html#hasGeospatialIssues): what coordinates issues are ignored (e.g. `COORDINATE_ROUNDED`)?
* `hasGeospatialIssues` is `false` for `COORDINATE_INVALID`. This seems like a bug.
* `hasGeospatialIssues` is `false` for `COORDINATE_REPROJECTION_FAILED`. Is this intentional?