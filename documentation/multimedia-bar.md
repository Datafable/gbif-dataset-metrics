# Multimedia bar

## Description

The multimedia bar groups the occurrences of a dataset in categories based on related multimedia. This functionality makes use of the [multimedia extension](http://rs.gbif.org/extension/gbif/1.0/multimedia.xml) in GBIF downloads, which contains all related multimedia, even those originally provided in `associatedMedia`. It allows the user to assess fitness for use and the data publisher to discover multimedia URL issues.

![screenshot](../images/features/multimedia-bar-995b2ca4-9b4d-4609-acd5-24d8297f0a4b.png)

## How we categorize

### Valid multimedia

The occurrence has one or more related multimedia (image, video, sound, or unknown type), *all* with a valid URL. The issue [MULTIMEDIA_DATE_INVALID](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/OccurrenceIssue.html#MULTIMEDIA_DATE_INVALID) is ignored.

### Multimedia URL invalid

The occurrence has the following issue: [MULTIMEDIA_URI_INVALID](http://gbif.github.io/gbif-api/apidocs/org/gbif/api/vocabulary/OccurrenceIssue.html#MULTIMEDIA_URI_INVALID), which is raised if *at least one* related multimedia has an invalid URL. 

### Multimedia not provided

The occurrence has no related multimedia available through GBIF.

## Suggestions for improvement

* Show the distribution of [multimedia type](http://gbif.github.io/dwc-api/apidocs/org/gbif/dwc/terms/GbifTerm.html#mediaType) (`StillImage`, `MovingImage`, `Sound`, and unknown type) for all related multimedia, so the user can discover what types of related multimedia a dataset contains. Note that this cannot be done as a distribution over occurrences, as one occurrence can have multiple related multimedia.
* Show the distribution of number of related multimedia per occurrence, so the user can assess if occurrences typically have one or more related multimedia.
* Display a sample or all related images of a dataset as thumbnails, so the user can get an impression of what was photographed (occurrences in their natural environment, herbarium scans, etc.).
