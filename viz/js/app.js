var main = function() {
    $.ajaxSetup({
        "async": false // Required so code waits for $.getJSON to be executed (async by default)
    });
    var datasetKey = "7f9eb622-c036-44c6-8be9-5793eaa1fa1e"; // Watervogels
    // var datasetKey = "271c444f-f8d8-4986-b748-e7367755c0c1"; // Florabank
    // var datasetKey = "4fa7b334-ce0d-4e88-aaae-2e0c138d049e"; // eBird

    $("#downloadCount").html(getDownloadsTotal(datasetKey) + " downloads"); // TODO: Add nice number formatting
    getDownloadsPerDay(datasetKey,50);
};

function getDayNumber(date) {
    var dayNumber = date.getTime();
    dayNumber = Math.floor(dayNumber / 1000 / 3600 / 24); // Floor on milliseconds, minutes and hours
    return dayNumber;
}

function getDownloadsTotal(datasetKey) {
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=1";
    var total = 0;
    $.getJSON(url, function(data) {
        total = data["count"];
    });
    return total;
}

function getDownloadsPerDay(datasetKey,dayRange) {
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=1000";
    // TODO: Need a way to loop over more pages
    $.getJSON(url, function(data) {
        var startDay = new Date();
            startDay = getDayNumber(startDay) - dayRange + 1;
        var labels = Array.apply(null, new Array(dayRange)).map(String.prototype.valueOf,"");;
        var days = Array.apply(null, new Array(dayRange)).map(Number.prototype.valueOf,0); // Populate array with zeroes
        
        $.each(data["results"],function(i,result) {
        var downloadDate = new Date(result["download"]["created"]);
            var downloadDay = getDayNumber(downloadDate);
            if (result["download"]["status"] == "SUCCEEDED" && downloadDay >= startDay) {
                days[downloadDay - startDay] += 1;
            }
        });

        // --- chart.js ---
        var data = {
            "labels": labels,
            "datasets": [
                {
                    // "label": "Downloads",
                    "fillColor": "#0099cc",
                    // "strokeColor": "rgba(220,220,220,0.8)",
                    "highlightFill": "rgba(220,220,220,0.75)",
                    "highlightStroke": "rgba(220,220,220,1)",
                    "data": days
                }
            ]
        };
        var ctx = $("#downloadChart").get(0).getContext("2d");
        var myBarChart = new Chart(ctx).Bar(data, {
            "scaleBeginAtZero": true,
            "scaleIntegersOnly": true, // Does this work?
            "scaleShowGridLines": false,
            "barShowStroke": false,
            "barStrokeWidth": 5,
            "barValueSpacing": 0,
            "showTooltips": false,
            "responsive": true
        });

        // --- c3.js ---
        var chart = c3.generate({
            bindto: "#chart",
            data: {
              columns: [
                ["downloads"].concat(days)
                // ["data",1,1,2,10]
              ],
              type: "bar"
            },
            bar: {
                width: {
                    ratio: 1
                }
            },
            axis: {
                x: {
                    show: true
                }
            },
            legend: {
                show: false
            }
        });
    });
}

$(document).ready(main);
