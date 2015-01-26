var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    loadMetricsData(datasetKey,showBasisOfRecordMetric,addBasisOfRecordToDOM);
}

var addBasisOfRecordToDOM = function(html) {
    $("#summary").find(".content").prepend(html);
}

main();
