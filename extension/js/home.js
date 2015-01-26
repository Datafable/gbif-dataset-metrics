var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    getMetrics(datasetKey,addMetricsToHomePage);
};

var addMetricsToHomePage = function (metrics) {
    // Create HTML
    var html = "";
    // Basis of record
    html = basisOfRecordBar(metrics);

    // Add HTML to page
    $("#summary").find(".content").prepend(html);

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
};

main();
