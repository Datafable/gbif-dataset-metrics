var main = function() {
    var datasetKey = getDatasetKeyFromURL();
    var datasetKey = "42319b8f-9b9d-448d-969f-656792a69176"; // Remove
    loadMetricsData(datasetKey,showBasisOfRecordMetric);
}

var showBasisOfRecordMetric = function(data) {
    var basisOfRecordsLabels = [
        "Preserved specimen",
        "Fossil specimen",
        "Living specimen",
        "Observation (unspecified)",
        "Human observation",
        "Machine observation",
        "Material sample",
        "Literature occurrence",
        "Unknown"
    ];
    var basisOfRecords = [
        data["bor_preserved_specimen"],
        data["bor_fossil_specimen"],
        data["bor_living_specimen"],
        data["bor_observation"],
        data["bor_human_observation"],
        data["bor_machine_observation"],
        data["bor_material_sample"],
        data["bor_literature"],
        data["bor_unknown"]
    ];

    var downloadChart = c3.generate({
        bindto: ".test",
        data: {
            columns: [
                ["basisOfRecords"].concat(basisOfRecords)
            ],
            type: "bar"
        },
        axis: {
            x: {
                type: "category",
                categories: basisOfRecordsLabels
            },
            y: {
                tick: {
                    outer: false
                }
            }
        },
        // padding: {
        //     left: 30 // To make room for y-axis labels on data loading
        // },
        bar: {
            width: {
                ratio: 0.9
            }
        },
        legend: {
            show: false
        }
    });
}




main();
