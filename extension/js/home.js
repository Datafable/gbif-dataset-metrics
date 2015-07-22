var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    getMetrics(datasetKey,addMetricsToHomePage);
};

var addMetricsToHomePage = function (metrics) {
    var html = "";
    var anchor = $("#summary");
    
    // Add basis of record bar
    html = html + basisOfRecordBar(metrics);
    anchor.find(".content").prepend(html);

    // Add achievements
    html = "";
    html = html + occurrencesAchievement(metrics); // Occurrences achievement
    html = html + georeferenceAchievement(metrics); // Georeference achievement
    html = html + multimediaAchievement(metrics); // Multimedia achievement
    if (html !== "") {
        $("#firstContent").append('<p id="achievements">' + html + '</p>');
    }

    // Add image thumbnails
    // html = imageThumbnails(metrics);
    // anchor.after(html);

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
};

var imageThumbnails = function (metrics) {
    var html = "",
        images = JSON.parse(metrics.images_sample),
        thumbnails = [];

    if (Object.keys(images).length === 0) {
        return html;
    } else {

        // var images = {
        //     1052605264: "http://static.inaturalist.org/photos/1464487/medium.JPG?1420431660",
        //     1052605230: "https://farm8.staticflickr.com/7545/16198002052_dcc548d4eb.jpg",
        //     1052605234: "https://farm9.staticflickr.com/8612/15578712533_7356631694.jpg",
        //     1052605311: "http://lh3.ggpht.com/-2wXMbN54vRE/VKodWTAzTqI/AAAAAAAAEDM/IwtsE-K5LxU/s512/IMG_2608.JPG",
        //     1052605303: "http://static.inaturalist.org/photos/1464583/medium.JPG?1420433811",
        //     1052605359: "http://static.inaturalist.org/photos/1464709/medium.JPG?1420437838",
        //     1052605333: "http://static.inaturalist.org/photos/1464708/medium.JPG?1420437814",
        //     1052605384: "http://static.inaturalist.org/photos/1464784/medium.JPG?1420440139",
        //     1052605366: "http://static.inaturalist.org/photos/1464727/medium.JPG?1420438564",
        //     1052605339: "http://static.inaturalist.org/photos/1464691/medium.JPG?1420436811"
        // };

        $.each (images, function (gbifID, url) {
            thumbnails.push('<a href="http://gbif.org/occurrence/' + gbifID + '" class="thumbnail"><img src="' + url + '" alt="Image for occurrence ' + gbifID + '"></a>');
        });

        html =  '<article id="imagesSample">' +
                        '<header></header>' +
                        '<div class="content">' +
                            '<div class="header"><div class="left"><h2>Images Sample</h2></div></div>' +
                            '<div class="fullwidth">' +
                                '<div class="thumbnails clearfix">' +
                                    thumbnails.join("") +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<footer></footer>' +
                    '</article>';
        return html;
    }
}; 

main();
