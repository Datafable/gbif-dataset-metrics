var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    loadMetricsData(datasetKey,showBasisOfRecordMetric);
}

var showBasisOfRecordMetric = function(metrics) {
    var occurrences = metrics["occurrences"];
    var basisOfRecords = {
        labels: [
            "Preserved specimens",
            "Fossil specimens",
            "Living specimens",
            "Material samples",
            "Observations",
            "Human observations",
            "Machine observations",
            "Literature occurrences",
            "Unknown"
        ],
        metrics: [
            metrics["bor_preserved_specimen"],
            metrics["bor_fossil_specimen"],
            metrics["bor_living_specimen"],
            metrics["bor_material_sample"],
            metrics["bor_observation"],
            metrics["bor_human_observation"],
            metrics["bor_machine_observation"],
            metrics["bor_literature"],
            metrics["bor_unknown"]
        ]
    };

    // Create HTML
    var html = '<div id="basisOfRecordMetric" class="progress">';
    for (var i = 0; i < basisOfRecords.metrics.length; i++) {
        var percentage = Math.round(basisOfRecords.metrics[i]/occurrences*100,1);
        html = html + '<div class="progress-bar basis-of-record-' + i + '" style="width: ' + percentage + '%" data-toggle="tooltip" data-placement="top" title="' + basisOfRecords.labels[i] + ' ' + percentage + '%"><span class="sr-only">' + basisOfRecords.labels[i] + '</span></div>';
    }
    var html = html + '</div>'

    // Add to DOM
    $("#summary").find(".content").prepend(html);

    // Enable tooltip
    $('[data-toggle="tooltip"]').tooltip();
}

main();
