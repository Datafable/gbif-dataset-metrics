# gbif-challenge-2015

Our entry for the GBIF challenge 2015

## Extracting data

The Data extraction module walks in a directory full of Darwin Core Archives, and for each one generate a simple report file in JSON format.

### Notes

- An archive/report can describe multiple datasets AND a specific dataset can be enclosed in several archives, hence the need for the "data aggregation and storage" module. That provides in return much flexibility in terms of data volume and horizontal scalability capabilities.
- Performance: at this step, we can easily extract data from Archives containing 17+ million records in a few minutes. There's still work in progress.

### Code

- [`data_extraction_module/data_extract.py`](/data_extraction_module/data_extract.py) is the main script. Its input/output directories are configured by constants (DATA_SOURCE_DIR and REPORTS_DIR). Its requirements are listed in [`data_extraction_module/requirements.txt`](/data_extraction_module/requirements.txt)

## Aggregating 

Next, all extracted metrics from the downloaded GBIF datasets will be aggregated and written to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics).

### Code

- [`src/aggregator.py`](/src/aggregator.py): contains two classes. The `ReportAggregator` class will read all json files in a given directory, and merge the data into one json structure (actually, that is a Python dict). This results in one set of metric counts per dataset. The `CartoDBWriter` will write the data to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics) using the [`requests package`](http://docs.python-requests.org/en/latest/).
- [`src/test_aggregate_reports.py`](/src/test_aggregate_reports.py): this file contains unit tests for the `ReportAggregator`. The easiest way to run these tests is by using the [`nose testing package`](https://nose.readthedocs.org/en/latest/).
- [`bin/aggregate_metrics.py`](/bin/aggregate_metrics.py): Python script to run from the command line. It will use the `ReportAggregator` and `CartoDBWriter` class to aggregate the data and write it to CartoDB. To use it, do:

```
aggregate_metrics.py <data directory> <settings.json>

    data directory:  this should point to a directory
                     containing chunks of metric data.
                     metric data should be in json and
                     ordered by dataset key.

    settings.json:   contains the `api_key` that will
                     be used to contact the cartodb API.
```

Make sure you have a `settings.json` file. That file should contain json data and store the CartoDB API key with the tag `api_key`.

## The Google Chrome plugin

Documentation about the Google Chrome plugin comes here
