var DatasetMetrics = {
    conf: {
        'statsPageBarContainer': $('#occmetrics').find('.fullwidth'),
        'statsPagePartitionContainer': $('#occmetrics'), // Partition will be appended at the end of this
        'partitionWidth': 874,
        'partitionHeight': 500
    }
};

var removeGBIFPies = function() {
    var anchor = $('#occmetrics');
    anchor.find('.pies').remove(); // Remove some default elements
};

var main = function () {
    var datasetKey = getDatasetKeyFromURL();

    removeGBIFPies();
    getMetrics(datasetKey, addMetricsToStatsPage, $('#content'), 'Dataset metrics extension: ');
};



main();
