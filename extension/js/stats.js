var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    getMetrics(datasetKey,addMetricsToStatsPage);
};

var addMetricsToStatsPage = function (metrics) {
    var html = "";
    var anchor = $("#occmetrics");

    // Add bar metrics
    html = html + '<h3>Basis of record</h3>' + basisOfRecordBar(metrics); // Basis of record
    // Media type
    html = html + '<h3>Coordinates</h3>' + coordinatesBar(metrics); // Coordinates
    html = html + '<h3>Taxon match</h3>' + taxonMatchBar(metrics); // Taxon match
    anchor.find(".pies").remove(); // Remove some default elements
    anchor.find(".fullwidth").append(html); // Add new metrics
    
    // Activate bar metrics tooltip
    $('[data-toggle="tooltip"]').tooltip();



};

main();
