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
    html = html + '<h3>Media</h3>' + mediaTypeBar(metrics);

    // Coordinates
    html = html + '<h3>Coordinates</h3>' + coordinatesBar(metrics);
    // Taxon match

    // Add HTML to page
    var anchor = $("#occmetrics").find(".content");
    anchor.find(".header").after(html);

    // Remove some default elements
    anchor.find(".pies li:nth-child(2)").remove();

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
};

main();
