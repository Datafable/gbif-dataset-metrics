# Data aggregation module

While analyzing the GBIF data, the downloaded file will be split into several files in order to process them. The extraction module will process these files and report dataset metrics per file. As a consequence, metric data from one dataset can be divided over multiple report files. The aggregation module will process all result files from the extraction module, and aggregate the metrics per dataset. The resulting metrics of the aggregation are pushed to a CartoDB table which serves as a backend for our Google Chrome plugin.

In order to run the aggregation module, put all report files from the extraction module (these are json files) in a single directory. Run the aggregation module from this directory with the command

```
python bin/aggregate_metrics.py path_to_data_directory settings.json
```

The `settings.json` file should contain the tag `api_key` containing the API key needed to write to the CartoDB table. The script will aggregate all metrics data in the `path_to_data_directory` and write the results to the CartoDB table. Every dataset key and response from the CartoDB API is written to the command line. Redirect this output to a file if subsequent analysis is required.
