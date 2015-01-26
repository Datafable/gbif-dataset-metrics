var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    getMetrics(datasetKey,addMetricsToStatsPage);
};

var addMetricsToStatsPage = function (metrics) {
    // Create HTML
    var html = "";
    // Basis of record
    html = html + '<h3>Basis of record</h3>' + basisOfRecordBar(metrics);
    // Media type

    // Coordinates
    html = html + '<h3>Coordinates</h3>' + coordinatesBar(metrics);
    // Taxon match
    html = html + '<h3>Taxon match</h3>' + taxonMatchBar(metrics);
    // Add HTML to page
    var anchor = $("#occmetrics").find(".content");
    anchor.find(".header").after(html);

    // Remove some default elements
    anchor.find(".pies li:nth-child(2)").remove();

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
};

main();
