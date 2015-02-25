# Extraction

The Data extraction module walks in a directory full of Darwin Core Archives, and for each one generate a simple report file in JSON format.

### Notes

- An archive/report can describe multiple datasets AND a specific dataset can be enclosed in several archives, hence the need for the "data aggregation and storage" module. That provides in return much flexibility in terms of data volume and horizontal scalability capabilities.
- Performance: at this step, we can easily extract data from Archives containing 17+ million records in a few minutes. There's still work in progress.

### Code

- [`data_extraction_module/data_extract.py`](/data_extraction_module/data_extract.py) is the main script. Its input/output directories are configured by constants (DATA_SOURCE_DIR and REPORTS_DIR). Its requirements are listed in [`data_extraction_module/requirements.txt`](/data_extraction_module/requirements.txt)
