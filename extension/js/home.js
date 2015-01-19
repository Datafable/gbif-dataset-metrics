var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    showBasisOfRecordChart(datasetKey);
}

var showBasisOfRecordChart = function(datasetKey) {
    datasetKey = "42319b8f-9b9d-448d-969f-656792a69176";
    var basisOfRecordList = [
        "PRESERVED_SPECIMEN",
        "FOSSIL_SPECIMEN",
        "LIVING_SPECIMEN",
        "OBSERVATION",
        "HUMAN_OBSERVATION",
        "MACHINE_OBSERVATION",
        "MATERIAL_SAMPLE",
        "LITERATURE",
        "UNKNOWN"
    ]
    var results = loadBasisOfRecordData(datasetKey, basisOfRecordList);
    console.log(results);
}

var getBasisOfRecordCount = function(datasetKey, basisOfRecord) {
    var d = when.defer();
    var url = "http://api.gbif.org/v1/occurrence/count?datasetKey=" + datasetKey + "&basisOfRecord=" + basisOfRecord;
    d3.json(url, function(error, result){
        if(error) d.reject(console.warn(error));
        d.resolve(result);
    });
    return d.promise;
}

var loadBasisOfRecordData = function(datasetKey, basisOfRecordList) {
    
    var basisOfRecordMetrics = [];
    for (var i = 0; i < basisOfRecordList.length; i++) {
        basisOfRecordMetrics.push(getBasisOfRecordCount(datasetKey, basisOfRecordList[i]));
    }
    return when.all(basisOfRecordMetrics);
}

main();
