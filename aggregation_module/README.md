# Aggregation module

Next, all extracted metrics from the downloaded GBIF datasets will be aggregated and written to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics).

## Code

- **Required Python packages:** [nesting](https://pypi.python.org/pypi/nesting/0.1.0), [requests](http://docs.python-requests.org/en/latest/)
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

---

While analyzing the GBIF data, the downloaded file will be split into several files in order to process them. The extraction module will process these files and report dataset metrics per file. As a consequence, metric data from one dataset can be divided over multiple report files. The aggregation module will process all result files from the extraction module, and aggregate the metrics per dataset. The resulting metrics of the aggregation are pushed to a CartoDB table which serves as a backend for our Google Chrome plugin.

In order to run the aggregation module, put all report files from the extraction module (these are json files) in a single directory. Run the aggregation module from this directory with the command

```
python bin/aggregate_metrics.py path_to_data_directory settings.json
```

The `settings.json` file should contain the tag `api_key` containing the API key needed to write to the CartoDB table. The script will aggregate all metrics data in the `path_to_data_directory` and write the results to the CartoDB table. Every dataset key and response from the CartoDB API is written to the command line. Redirect this output to a file if subsequent analysis is required.
