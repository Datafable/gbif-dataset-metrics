# Aggregation module

## Description

Since the [extraction module](../extraction_module) can result in metrics of a single dataset being divided over different output files, the aggregation module was implemented to aggregate the metrics of each dataset. Once these metrics are aggregated, the aggretion module will constructs a taxonomy tree for each dataset. The metrics and the taxonomy tree are written to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics) that will serve as a back end for the [extension](../extension).

## Requirements

- [nesting](https://pypi.python.org/pypi/nesting/0.1.0). This package is used to construct the taxonomy tree.
- [requests](http://docs.python-requests.org/en/latest/). This package is used to communicate with the CartoDB API.

## Components

- [`src/aggregator.py`](./src/aggregator.py): contains two classes. The `ReportAggregator` class will read all json files in a given directory, and merge the data into one json structure (actually, that is a Python dict). This results in one set of metric counts per dataset. The `CartoDBWriter` will write the data to a [CartoDB table](https://datafable.cartodb.com/tables/gbif_dataset_metrics) using the [`requests package`](http://docs.python-requests.org/en/latest/).
- [`src/test_aggregate_reports.py`](/src/test_aggregate_reports.py): this file contains unit tests for the `ReportAggregator`. The easiest way to run these tests is by using the [`nose testing package`](https://nose.readthedocs.org/en/latest/).
- [`bin/aggregate_metrics.py`](/bin/aggregate_metrics.py): Python script to run from the command line. It will use the `ReportAggregator` and `CartoDBWriter` class to aggregate the data and write it to CartoDB.

## To run

1. Install the requirements:

```
$ pip install nesting
$ pip install requests
```

2. Put all the output files of the [extraction module](../extraction_module) in a single directory. Make sure no other json files are in there.
3. Create a `settings.json` file. That file should contain json data and store the CartoDB API key with the tag `api_key`.
4. Run the aggregator:

```
python aggregate_metrics.py <data directory> <settings.json>

    data directory:  this should point to a directory
                     containing chunks of metric data.
                     metric data should be in json and
                     ordered by dataset key.

    settings.json:   contains the `api_key` that will
                     be used to contact the cartodb API.
```

The script will aggregate all metrics data in the `path_to_data_directory` and write the results to the CartoDB table. Every dataset key and response from the CartoDB API is written to the command line. Redirect this output to a file if subsequent analysis is required.
