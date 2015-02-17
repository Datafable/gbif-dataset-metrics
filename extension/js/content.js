var getDatasetKeyFromURL = function () {
    var pathArray = window.location.pathname.split('/'),
        datasetKey = "";
    if (pathArray[1] === "dataset") { // On GBIF website, get datasetKey from URL.
        datasetKey = pathArray[2];
    } else { // Elsewhere, e.g. demo pages, use demo datasetKey.
        datasetKey = "42319b8f-9b9d-448d-969f-656792a69176"; // Coccinellidae
    }
    return datasetKey;
};

var addAboveContent = function () {
    var html = '<article id="aboveContent"></content>';
    $("#content").prepend(html);
};

var addNoMetricsMessage = function () {
    var html = '<p class="alert alert-warning"><strong>GBIF dataset metrics extension:</strong> We have no metrics for this dataset yet. Want some? <a href="https://github.com/peterdesmet/gbif-challenge/issues/new" target="_blank">Submit a request.</a></p>';
    $("#aboveContent").append(html);
};

var getMetrics = function (datasetKey, showMetrics) {
    // Get data from metrics store in CartoDB.
    var sql = "WITH ranked_metrics AS ( SELECT *, ntile(100) OVER (ORDER BY occurrences) AS occurrences_percentile FROM gbif_dataset_metrics_test WHERE type = 'OCCURRENCE' AND occurrences IS NOT NULL) SELECT * FROM ranked_metrics WHERE dataset_key ='" + datasetKey + "'"
    var url = "http://datafable.cartodb.com/api/v2/sql?q=" + sql;
    $.getJSON(url, function (result) {
        if (result.rows.length === 0) { // Dataset is not in query: not OCCURRENCE, no data yet or a new dataset
            addNoMetricsMessage();
        } else {
            showMetrics(result.rows[0]); // Only one row [0] expected
        }
    });
};

var createAchievementLabel = function (achievement, title, rank) {
    return '<span class="label ' + rank + '" data-toggle="tooltip" data-placement="top" title="' + title + '">' + achievement + '</span> ';
};

var occurrencesAchievement = function (metrics) {
    var html = "";
    var rank = metrics.occurrences_percentile;
    if (rank > 90) {
        html = createAchievementLabel("Colossal dataset", "In the top 10% biggest datasets on GBIF", "gold");
    } else if (rank > 80) {
        html = createAchievementLabel("Huge dataset", "In the top 20% biggest datasets on GBIF", "silver");
    }
    return html;
};

var georeferenceAchievement = function (metrics) {
    var html = "";
    var rank = metrics.coordinates_valid / metrics.occurrences;
    console.log(rank);
    if (rank === 1) {
        html = createAchievementLabel("Georeferencing perfection", "100% valid coordinates", "gold");
    } else if (rank > 0.95) {
        html = createAchievementLabel("Georeferencing excellence", " More than 95% valid coordinates", "silver");
    }
    return html;
};

var multimediaAchievement = function (metrics) {
    var html = "";
    var rank = metrics.multimedia_valid / metrics.occurrences;
    console.log(rank);
    if (rank > 0.75) {
        html = createAchievementLabel("Multimedia treasure", "More than 75% related multimedia", "gold");
    } else if (rank >= 0.50) {
        html = createAchievementLabel("Multimedia gem", " More than 50% related multimedia", "silver");
    }
    return html;
};

var createMetricBar = function (metric) {
    // Create HTML for a metric, using Bootstrap progress bar.
    var html = '<div class="progress">';
    for (var i = 0; i < metric.counts.length; i++) {
        var occurrences = parseInt(metric.counts[i]).toLocaleString();
        var percentage = metric.counts[i]/metric.total*100;
        html = html + '<div class="progress-bar ' + metric.cssClass + '-' + i + '" style="width: ' + percentage + '%" data-toggle="tooltip" data-placement="top" title="' + metric.labels[i] + ' ' + percentage.toFixed(1) + '% (' + occurrences +')"><span class="sr-only">' + metric.labels[i] + '</span></div>';
    }
    html = html + '</div>';
    return html;
};

var basisOfRecordBar = function (metrics) {
    var metric = {
        cssClass: "basis-of-record",
        total: metrics.occurrences,
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
        counts: [
            metrics.bor_preserved_specimen,
            metrics.bor_fossil_specimen,
            metrics.bor_living_specimen,
            metrics.bor_material_sample,
            metrics.bor_observation,
            metrics.bor_human_observation,
            metrics.bor_machine_observation,
            metrics.bor_literature,
            metrics.bor_unknown
        ]
    };
    return createMetricBar(metric);
};

var coordinatesBar = function (metrics) {
    var metric = {
        cssClass: "coordinates",
        total: metrics.occurrences,
        labels: [
            "Valid coordinates (all in WGS84)",
            "Coordinates with minor issues",
            "Coordinates with major issues",
            "Coordinates not provided"
        ],
        counts: [
            metrics.coordinates_valid,
            metrics.coordinates_minor_issues,
            metrics.coordinates_major_issues,
            metrics.coordinates_not_provided
        ]
    };
    return createMetricBar(metric);
};

var multimediaBar = function (metrics) {
    var metric = {
        cssClass: "multimedia",
        total: metrics.occurrences,
        labels: [
            "Valid multimedia",
            "Multimedia URL invalid",
            "Multimedia not provided"
        ],
        counts: [
            metrics.multimedia_valid,
            metrics.multimedia_url_invalid,
            metrics.multimedia_not_provided
        ]
    };
    return createMetricBar(metric);
};

var taxonMatchBar = function (metrics) {
    var metric = {
        cssClass: "taxon-match",
        total: metrics.occurrences,
        labels: [
            "Taxon found in taxonomic backbone",
            "Taxon found in taxonomic backbone using fuzzy match",
            "Taxon not found in taxonomic backbone, but a higher taxon was",
            "Taxon not found in taxonomic backbone",
            "Taxon not provided"
        ],
        counts: [
            metrics.taxon_match_complete,
            metrics.taxon_match_fuzzy,
            metrics.taxon_match_higherrank,
            metrics.taxon_match_none,
            metrics.taxon_not_provided
        ]
    };
    return createMetricBar(metric);
};