var main = function() {
    var datasetKey = "7f9eb622-c036-44c6-8be9-5793eaa1fa1e"; // Watervogels
    var datasetKey = "271c444f-f8d8-4986-b748-e7367755c0c1"; // Florabank
    // var datasetKey = "4fa7b334-ce0d-4e88-aaae-2e0c138d049e"; // eBird

    showTotalDownloads(datasetKey);
    showDownloadsChart(datasetKey,30,1000);
};

function showTotalDownloads(datasetKey) {
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=1";
    d3.json(url,function(error,json) {
        if(error) return console.warn(error);

        var total = json["count"]; // Total number of downloads
        d3.select("#totalDownloads")
            .text(total);
    });
}

function showDownloadsChart(datasetKey,dayRange,limit) {
    // Note: this function does only one call to the GBIF API, so if dayRange is high and limit low, it might not retrieve all downloads
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=" + limit;
    console.log(url);
    d3.json(url,function(error,json) {
        if(error) return console.warn(error);

        for (var i = 0, days = new Array(dayRange); i < dayRange;) days[i++] = null; // Create null filled array "days" with length dayRange
        
        var startDay = new Date();
            startDay = getDayNumber(startDay) - dayRange + 1;

        json["results"].every(function(result) {
            var downloadDate = new Date(result["download"]["created"]);
            var downloadDay = getDayNumber(downloadDate);
            if (downloadDay >= startDay) {
                if (result["download"]["status"] == "SUCCEEDED") {
                    days[downloadDay - startDay] += 1;
                }
                return true; // Continue looping
            } else {
                return false; // Stop looping, since loop passed beyond startDay. Assumes json is returned in reversed chronology.
            }
        });

        // Create chart
        var chart = c3.generate({
            bindto: "#downloadsChart",
            data: {
                columns: [
                    ["downloads"].concat(days)
                ],
                type: "bar"
            },
            axis: {
                x: {
                    show: false
                },
                y: {
                    tick: {
                        format: function(x) {
                            return (x == Math.floor(x)) ? x : "";
                        }
                    }
                }
            },
            legend: {
                show: false
            },
            interaction: {
                enabled: false
            },
            bar: {
                width: {
                    ratio: 1
                }
            }
        });
    });
}

function getDayNumber(date) {
    var dayNumber = date.getTime();
    dayNumber = Math.floor(dayNumber / 1000 / 3600 / 24); // Floor on milliseconds, minutes and hours
    return dayNumber;
}

$(document).ready(main);
