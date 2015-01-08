var main = function() {
    console.log(getDatasetKeyFromURL());
    removeDownloadBox();
    addChart();
    console.log(document.URL);
}

var getDatasetKeyFromURL = function() {
    var pathArray = window.location.pathname.split('/'); // /dataset/key/*
    var datasetKey = pathArray[2]; // 0 is empty, second is "dataset"
    return datasetKey;
}

var removeDownloadBox = function() {
    var downloadBox = $("#infoband").find(".content .box");
    downloadBox.fadeOut(2000);
}

var addChart = function() {
    var hook = $("#content").find(".content .header");
    hook.after('<div id="downloadChart">Hello</div>').addClass("red");
}

$(document).ready(main);
