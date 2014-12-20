var main = function() {
    var datasetKey = "7f9eb622-c036-44c6-8be9-5793eaa1fa1e"; // Watervogels
    var datasetKey = "271c444f-f8d8-4986-b748-e7367755c0c1"; // Florabank
    getDownloads(datasetKey);
};

function getDownloads(datasetKey) {
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=100";
    console.log(url);
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=1000";
    $.getJSON(url, function(data) {
        var downloadCount = data["count"];
        var occurrenceCount = 0;

        var currentDate = new Date();
        var startDate = new Date();
            startDate.setUTCMonth(startDate.getUTCMonth() - 11); // Go back 11 months from current date (= a year ago)
            startDate.setUTCDate("01"); // Set at first day of month
            startDate.setUTCHours(0,0,0,0); // Set at midnight

        var labels = [1,2,3,4,5,6,7,8,9,10,11,12]; // TODO: Should be dynamic.
        var downloadsPerMonth = [0,0,0,0,0,0,0,0,0,0,0,0];
        var occurrencesPerMonth = [0,0,0,0,0,0,0,0,0,0,0,0];

        $.each(data["results"],function(i,result) {
            occurrenceCount = occurrenceCount + result["numberRecords"];
            var downloadDate = new Date(result["download"]["created"]);
            var downloadMonth = downloadDate.getUTCMonth();

            if (result["download"]["status"] == "SUCCEEDED" && downloadDate >= startDate) {
                downloadsPerMonth[downloadMonth] = downloadsPerMonth[downloadMonth] + 1;
                occurrencesPerMonth[downloadMonth] = occurrencesPerMonth[downloadMonth] + result["numberRecords"];
            }
        });

        $("#downloadCount").html(downloadCount + " downloads"); // TODO: Add nice number formatting
        $("#downloadRecordCount").html(occurrenceCount + " records"); // TODO: Add nice number formatting


        var data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Downloads",
                    "fillColor": "rgba(220,220,220,0.5)",
                    "strokeColor": "rgba(220,220,220,0.8)",
                    "highlightFill": "rgba(220,220,220,0.75)",
                    "highlightStroke": "rgba(220,220,220,1)",
                    "data": downloadsPerMonth
                },
                // {
                //     "label": "Occurrences",
                //     "fillColor": "rgba(151,187,205,0.5)",
                //     "strokeColor": "rgba(151,187,205,0.8)",
                //     "highlightFill": "rgba(151,187,205,0.75)",
                //     "highlightStroke": "rgba(151,187,205,1)",
                //     "data": occurrencesPerMonth
                // }
            ]
        };
        var ctx = $("#downloadChart").get(0).getContext("2d");
        var myBarChart = new Chart(ctx).Bar(data, {});
    });
}


$(document).ready(main);
