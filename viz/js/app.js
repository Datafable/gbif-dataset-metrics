var main = function() {
    // var datasetKey = "7f9eb622-c036-44c6-8be9-5793eaa1fa1e"; // Watervogels
    // var datasetKey = "271c444f-f8d8-4986-b748-e7367755c0c1"; // Florabank
    var datasetKey = "4fa7b334-ce0d-4e88-aaae-2e0c138d049e"; // eBird

    showDownloadsTotal(datasetKey);
    showDownloadsChart(datasetKey,30);
};

function showDownloadsTotal(datasetKey) {
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=1";
    d3.json(url,function(error,json) {
        if(error) return console.warn(error);

        var total = json["count"]; // Total number of downloads
        d3.select("#downloadsTotal")
            .text(total);
    });
}

function removeTimeFromDate(date) {
        return date.setUTCHours(0,0,0,0); // Floor date to midnight and return as time integer
    }

function formatAsISODate(time) {
        var date = new Date(time);
        return date.toISOString().substring(0,10); // Return first 10 characters (yyyy-mm-dd) of full ISO date
    }

function showDownloadsChart(datasetKey,dayRange) {
    var oneDayInMs = 24 * 60 * 60 * 1000;
    var today = new Date();
    var startDay = removeTimeFromDate(today); // Set at midnight
        startDay = startDay - ((dayRange - 1) * oneDayInMs); // Substract dayRange in milliseconds
    var days = new Array();
    var downloads = new Array();
    for (var i = 0; i < dayRange; i++) {
        days[i] = formatAsISODate(startDay + i * oneDayInMs); // Populate array with all dates in ISO8601
        downloads[i] = null; // Populate array with null values (for empty chart)
    }

    var downloadChart = c3.generate({
        bindto: "#downloadsChart",
        data: {
            x: "days",
            columns: [
                ["days"].concat(days),
                ["downloads"].concat(downloads)
            ],
            type: "bar"
        },
        axis: {
            x: {
                type: "timeseries",
                show: false,
                tick: {
                    format: "%Y-%m-%d"
                }
            },
            y: {
                tick: {
                    outer: false
                }
            }
        },
        padding: {
            left: 30 // To make room for labels on data loading
        },
        bar: {
            width: {
                ratio: 0.9
            }
        },
        legend: {
            show: false
        }
    });

    loadDownloads(datasetKey,1000,startDay,oneDayInMs,downloads,downloadChart); // Load data
}

function loadDownloads(datasetKey,pageLimit,startDay,oneDayInMs,downloads,downloadChart) {
    /*  Note: this function does only one call to the GBIF API, so if dayRange 
        is high and pageLimit low, it might not retrieve all downloads. */
    
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=" + pageLimit;
    d3.json(url,function(error,json) {
        if(error) return console.warn(error);

        json["results"].every(function(result) {
            var downloadDay = removeTimeFromDate(new Date(result["download"]["created"]));
            // console.log(downloadDay);
            
            if (downloadDay >= startDay) {
                if (result["download"]["status"] == "SUCCEEDED") {
                    var i = (downloadDay - startDay) / oneDayInMs; // Day index
                    downloads[i] += 1;
                }
                return true; // Continue looping
            } else {
                return false; // Passed beyond startDay, stop looping. Assumes API returns downloads in reversed chronology.
            }
        });

        downloadChart.load({
            columns: [
                ["downloads"].concat(downloads)
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
