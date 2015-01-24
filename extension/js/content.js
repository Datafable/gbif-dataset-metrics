var getDatasetKeyFromURL = function() {
    var pathArray = window.location.pathname.split('/');
    var datasetKey = pathArray[2]; // Parsing path: 0 is empty, second is "dataset".
    return datasetKey;
}

var loadMetricsData = function(datasetKey, showMetric) {
    // Get data from metrics store in CartoDB.
    var url = "http://peterdesmet.cartodb.com/api/v2/sql?q=SELECT * FROM gbif_dataset_metrics WHERE dataset_key ='" + datasetKey + "'";
    d3.json(url,function(error, result){
        if (error) return console.warn(error);
        if (result["rows"] == "") {
            console.log("No metrics for this dataset");
        } else {
            result["rows"].every(function(data) {
                showMetric(data);
                return false; // Don't loop, only one row expected.
            });
        }
    });
}
