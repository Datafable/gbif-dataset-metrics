var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    getMetrics(datasetKey,addMetricsToHomePage);
};

var addMetricsToHomePage = function (metrics) {
    var html = '';
    var anchor = $('#summary');
    
    // Add basis of record bar
    html = html + basisOfRecordBar(metrics);
    anchor.find('.content').prepend(html);

    // Add achievements
    html = '';
    html = html + occurrencesAchievement(metrics); // Occurrences achievement
    html = html + georeferenceAchievement(metrics); // Georeference achievement
    html = html + multimediaAchievement(metrics); // Multimedia achievement
    if (html !== '') {
        $('#firstContent').append('<p id="achievements">' + html + '</p>');
    }

    // Add image thumbnails
    html = imageThumbnails(metrics);
    anchor.after(html);

    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
};

var imageThumbnails = function (metrics) {
    var html = "",
        images = JSON.parse(metrics.images_sample),
        thumbnails = [];

    if (images !== null) {
        // Create list of thumbnails with non-empty links
        $.each (images, function (gbifID, url) {
            if (url !== '') {
                thumbnails.push('<a href="http://gbif.org/occurrence/' + gbifID + '" class="thumbnail"><img src="' + url + '" alt="Image for occurrence ' + gbifID + '"></a>');
            }
        });

        // If thumbnails available, add an images section
        if (thumbnails.length > 0) {
            html =  '<article id="imagesSample">' +
                            '<header></header>' +
                            '<div class="content">' +
                                '<div class="header"><div class="left"><h2>Sample of images</h2></div></div>' +
                                '<div class="fullwidth">' +
                                    '<div class="thumbnails clearfix">' +
                                        thumbnails.join('') +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<footer></footer>' +
                        '</article>';
        }
    }
    return html;
}; 

main();
