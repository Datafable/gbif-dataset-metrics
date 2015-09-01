# Sample of images

## Description

Darwin Core Archives may contain links to multimedia files related to the dataset. Some of these, labelled `StillImages` ([see multimedia type documentation](http://gbif.github.io/dwc-api/apidocs/org/gbif/dwc/terms/GbifTerm.html#mediaType)) may contain images of the actual occurrences. The sample of images feature inserts a random sample of maximum 20 images in the dataset page which can be extremely informative for potential data users. When a user clicks on an image, he will be directed to the corresponding occurrence page.

![screenshot](../images/features/sample-of-images-85930e96-f762-11e1-a439-00145eb45e9a.png)

## How it works

Multimedia urls are extracted from the Darwin Core multimedia extension. For every dataset, only the `StillImages` are considered, and a random sample of 20 occurrences are selected. If an occurrence contains multiple links to images, one is picked randomly. The random sample of images is written to the datastore and displayed on the dataset page.

## Suggestions for improvement

* Determine the file types used in `NoType` as this category frequently contains images too.
* Support the other multimedia types too.

