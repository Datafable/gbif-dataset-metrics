var getDatasetKeyFromURL = function() {
    var pathArray = window.location.pathname.split('/');
    if (pathArray[1] == "dataset") {
        // On GBIF website, get datasetKey from URL.
        var datasetKey = pathArray[2];
    } else {
        // Elsewhere, e.g. demo pages, use demo datasetKey.
        var datasetKey = "42319b8f-9b9d-448d-969f-656792a69176"; // Coccinellidae
    }
    return datasetKey;
}

var loadMetricsData = function(datasetKey, showMetric) {
    // Get data from metrics store in CartoDB.
    var url = "http://datafable.cartodb.com/api/v2/sql?q=SELECT * FROM gbif_dataset_metrics WHERE dataset_key ='" + datasetKey + "'";
    $.getJSON(url,function(result) {
        if (result["rows"] == "") {
            console.log("No metrics for this dataset");
        } else {
            showMetric(result["rows"][0]); // Only one row [0] expected
        }
    });
}
