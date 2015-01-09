var getDatasetKeyFromURL = function() {
    var pathArray = window.location.pathname.split('/');
    var datasetKey = pathArray[2]; // 0 is empty, second is "dataset"
    return datasetKey;
}
