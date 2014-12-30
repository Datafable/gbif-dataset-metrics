var main = function() {
    var datasetKey = "7f9eb622-c036-44c6-8be9-5793eaa1fa1e"; // Watervogels
    // var datasetKey = "271c444f-f8d8-4986-b748-e7367755c0c1"; // Florabank
    // var datasetKey = "4fa7b334-ce0d-4e88-aaae-2e0c138d049e"; // eBird

    showTotalDownloads(datasetKey);

    createDownloadChart(datasetKey);
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

function createDownloadChart(datasetKey) {
    var downloadChart = c3.generate({
        bindto: "#downloadsChart",
        data: {
            x: "x",
            columns: [
                ["x","2014-12-13"],
                ["downloads",12]
            ],
            type: "bar"
        },
        axis: {
            x: {
                type: "timeseries",
                tick: {
                    format: "%Y-%m-%d"
                }
            }
        },
        bar: {
            width: {
                ratio: 0.5
            }
        },
        legend: {
            show: false
        }
    });

    getDownloads(datasetKey,new Date(),30,100,downloadChart); // Load data
}

function getDownloads(datasetKey,endDate,dayRange,limit,downloadChart) {
    function midnightDateTime(date) {
        return date.setUTCHours(0,0,0,0); // Floor date to midnight and return as time integer
    }
    function ISODateString(time) {
        var date = new Date(time);
        return date.toISOString().substring(0,10); // Return first 10 characters (yyyy-mm-dd) of full ISO date
    }

    var millisecondsRange = (dayRange - 1) * 24 * 3600 * 1000 // dayRange in milliseconds
    var startDateTime = midnightDateTime(endDate) - millisecondsRange;
    var endDateTime = midnightDateTime(endDate);
    
    // Note: this function does only one call to the GBIF API, so if dayRange is high and limit low, it might not retrieve all downloads
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=" + limit;
    d3.json(url,function(error,json) {
        if(error) return console.warn(error);

        var days = {};
        json["results"].every(function(result) {
            var downloadDateTime = midnightDateTime(new Date(result["download"]["created"]));
            
            if (downloadDateTime >= startDateTime) {
                if (result["download"]["status"] == "SUCCEEDED") {
                    var key = ISODateString(downloadDateTime); // Create key of form yyyy-mm-dd
                    if (key in days) {
                        days[key] += 1;
                    } else {
                        days[key] = 1; // Start new key
                    }
                }
                return true; // Continue looping
            } else {
                return false; // Stop looping, since loop passed beyond startDateTime. Assumes API returns downloads in reversed chronology.
            }
        });

        var daysKeys = Object.keys(days);
        var daysValues = new Array;
        for (var i = 0; i < daysKeys.length; i++) {
            daysValues[i] = days[daysKeys[i]];
        }

        downloadChart.load({
            columns: [
                ["x"].concat(daysKeys),
                ["downloads"].concat(daysValues)
            ]
        });
    });
}

function getDayNumber(date) {
    var dayNumber = date.getTime();
    dayNumber = Math.floor(dayNumber / 1000 / 3600 / 24); // Floor on milliseconds, minutes and hours
    return dayNumber;
}

main(); // No need to use $(document).ready(main);
