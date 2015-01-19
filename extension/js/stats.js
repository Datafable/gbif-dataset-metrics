var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    loadMetricsData();
}

var loadMetricsData = function(datasetKey) {
    datasetKey = "42319b8f-9b9d-448d-969f-656792a69176"; /* Remove this */
    
    var url = "http://peterdesmet.cartodb.com/api/v2/sql?q=SELECT * FROM gbif_dataset_metrics WHERE dataset_key ='" + datasetKey + "'";
    d3.json(url,function(error, result){
        if(error) return console.warn(error);

        result["rows"].every(function(rows) {
            var basisOfRecord = rows["basis_of_record"]; // JSON
            var coordinatesQuality = rows["coordinates_quality"]; // JSON

            console.log(basisOfRecord);
            console.log(coordinatesQuality);
        });
    });
}

main();
