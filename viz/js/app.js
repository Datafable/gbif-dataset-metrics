var main = function() {
    var datasetKey = "7f9eb622-c036-44c6-8be9-5793eaa1fa1e"; // Watervogels
    var datasetKey = "271c444f-f8d8-4986-b748-e7367755c0c1"; // Florabank
    getDownloads(datasetKey);
};

function getDownloads(datasetKey) {
    var url = "http://api.gbif.org/v1/occurrence/download/dataset/" + datasetKey + "?limit=100";
    console.log(url);
    $.getJSON(url, function(data) {
        var count = data["count"];
        console.log(count);
        $("#downloadCount").html(count);
    });

}

$(document).ready(main);
