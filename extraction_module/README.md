# Extraction module

## Description

The extraction module calculates the metrics from the occurrences. It crawls a directory containing Darwin Core Archives (downloaded from the [GBIF website](http://www.gbif.org)) and for each one generates a simple report file containing "raw metrics" in JSON format. These JSON reports will then be used as the input of the [aggregation module](../aggregation_module).

## Notes

* One archive/report can describe multiple datasets AND a specific dataset can be enclosed in several archives, hence the need for the aggregation module. That provides in return a lot of flexibility in terms of data volume and horizontal scalability capabilities.
* At this stage, we are able to process 7GB+ compressed archives in a couple of hours on a standard Macbook Pro. Performance is still incrementally being improved and we expect ultimately to be able to parse all GBIF occurrence data.
* This module is very concise since the hard/low-level work is delegated to [python-dwca-reader](http://python-dwca-reader.readthedocs.org/).

## Requirements

[python-dwca-reader](http://python-dwca-reader.readthedocs.org/) (and indirectly Beautifulsoup and lxml)

## To run

1. Install the requirements: `$ pip install -r requirements.txt`
2. Download data from GBIF (search per dataset or per publishing country for example) and place the Darwin Core Archives (zip files) in an empty directory.
3. Create another empty directory somewhere else to receive the reports.
4. Configure these two directories in `DATA_SOURCE_DIR` and `REPORTS_DIR`(at the top of `bin/extract_data.py`)
5. Run the extractor: `$ python bin/extract_data.py`.
6. That's it! You can now use the generated reports in the [aggregation module](../aggregation_module).
