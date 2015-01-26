var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    loadMetricsData(datasetKey,showBasisOfRecordMetric,addBasisOfRecordToDOM);
}

var addBasisOfRecordToDOM = function(html) {
    $("#occmetrics").find(".content .pies").prepend(html);
}

main();
