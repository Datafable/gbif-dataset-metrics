var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    
    var metricsHTML = '<div id="basisOfRecordMetric"></div>';
    var occmetricsAnchor = $("#occmetrics").find(".content");
    occmetricsAnchor.find(".header").after(metricsHTML); // Add scaffolding for metrics
    occmetricsAnchor.find(".pies li:nth-child(2)").remove(); // Remove default basis of record pie chart
    
    loadMetricsData(datasetKey,showBasisOfRecordMetric,addBasisOfRecordToDOM);
}

var addBasisOfRecordToDOM = function(html) {
    html = '<h3 class="metric-title">Basis of record</h3>' + html;
    $("#basisOfRecordMetric").append(html);
}

main();
