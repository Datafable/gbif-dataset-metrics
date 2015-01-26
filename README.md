# gbif-challenge-2015

Our entry for the GBIF challenge 2015

## Extracting data

Documentation about the extraction modules comes here

## Aggregating 

Next, all extracted metrics from the downloaded GBIF datasets will be aggregated and written to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics).

### Code

- [`src/aggregator.py`](/src/aggregator.py): contains two classes. The `ReportAggregator` class will read all json files in a given directory, and merge the data into one json structure (actually, that is a Python dict). This results in one set of metric counts per dataset. The CartoDBWriter will write the data to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics) using the [`requests package`](http://docs.python-requests.org/en/latest/).
- [`src/test_aggregate_reports.py`](/src/test_aggregate_reports.py): this file contains unit tests for the `ReportAggregator`. The easiest way to run these tests is by using the [`nose testing package`](https://nose.readthedocs.org/en/latest/).

## The Google Chrome plugin

Documentation about the Google Chrome plugin comes here
