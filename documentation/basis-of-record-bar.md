# Basis of record bar

## Description

The basis of record bar groups the occurrences of a dataset in categories based on the [basis of record](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html).

![screenshot](../images/features/basis-of-record-bar-42319b8f-9b9d-448d-969f-656792a69176.png)

## How we categorize

The occurrences are categorized based on their [basis of record Enum](basis-of-record-bar-42319b8f-9b9d-448d-969f-656792a69176). For each basis of record we use a distinct colour, but use similar colours for similar basis of records. We do not use the [BASIS_OF_RECORD_INVALID](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/OccurrenceIssue.html#BASIS_OF_RECORD_INVALID) issue, as those occurrences are assigned `UNKNOWN` by GBIF.

* [Preserved specimens](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#PRESERVED_SPECIMEN): yellow
* [Fossil specimens](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#FOSSIL_SPECIMEN): lighter yellow
* [Living specimens](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#LIVING SPECIMEN): lightest yellow
* [Material samples](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#MATERIAL_SAMPLE): purple
* [Observations](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#OBSERVATION): blue
* [Human observations](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#HUMAN_OBSERVATION): lighter blue
* [Machine observations](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#MACHINE_OBSERVATION): lightest blue
* [Literature occurrences](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#LITERATURE): pink
* [Unknown](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/BasisOfRecord.html#UNKNOWN): grey

## Suggestions for GBIF

Since unrecognized basis of records are transformed to `UNKNOWN`, is the issue `BASIS_OF_RECORD_INVALID` still useful? A [search for those occurrences returns 0 results](http://www.gbif.org/occurrence/search?ISSUE=BASIS_OF_RECORD_INVALID).
