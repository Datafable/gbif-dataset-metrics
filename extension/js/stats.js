var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    getMetrics(datasetKey,addMetricsToStatsPage);
};

var addMetricsToStatsPage = function (metrics) {
    var html = "";
    var anchor = $("#occmetrics");

    // Add bar metrics
    html = html + '<h3>Basis of record</h3>' + basisOfRecordBar(metrics); // Basis of record
    // Media type
    html = html + '<h3>Coordinates</h3>' + coordinatesBar(metrics); // Coordinates
    html = html + '<h3>Taxon match</h3>' + taxonMatchBar(metrics); // Taxon match
    anchor.find(".pies").remove(); // Remove some default elements
    anchor.find(".fullwidth").append(html); // Add new metrics
    
    // Activate bar metrics tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // Add taxonomy partition
    html = '<article id="taxonomy">' + 
                '<header></header>' + 
                '<div class="content">' + 
                    '<div class="header"><div class="left"><h2>Taxonomy</h2></div></div>' +
                    '<div class="fullwidth"></div>' +
                '</div>' +
                '<footer></footer>' + 
            '</article>';
    anchor.after(html);
    taxonomyPartition(metrics);
};

var taxonomyPartition = function (metrics) {
    // Based on http://bl.ocks.org/mbostock/1005873
    var width = 874,
        height = 250;

    var x = d3.scale.linear().range([0, width]),
        y = d3.scale.linear().range([0, height]),
        color = d3.scale.ordinal().range(colorbrewer.Blues[5]); // BuGn, YlGn, YlGnBu, PuBu, Blues, RdYlGn

    var partition = d3.layout.partition()
        .children(function (d) { return isNaN(d.value) ? d3.entries(d.value) : null; })
        .value(function (d) { return d.value; });

    var svg = d3.select("#taxonomy .fullwidth").append("svg")
        .attr("width", width)
        .attr("height", height);

    var rect = svg.selectAll("rect");

    d3.json("taxonomy.json", function (error, root) {
        rect = rect
            .data(partition(d3.entries(root)[0]))
            .enter().append("rect")
            .attr("x", function (d) { return x(d.x); })
            .attr("y", function (d) { return y(d.y); })
            .attr("width", function (d) { return x(d.dx); })
            .attr("height", function (d) { return y(d.dy); })
            .attr("fill", function (d) { return color((d.children ? d : d.parent).key); })
            .on("click", clicked);
    });

    function clicked (d) {
        x.domain([d.x, d.x + d.dx]);
        // y.domain([d.y, 1]).range([d.y ? 20 : 0, height]);

        rect.transition()
            .duration(600)
            .attr("x", function (d) { return x(d.x); })
            //.attr("y", function (d) { return y(d.y); })
            .attr("width", function (d) { return x(d.x + d.dx) - x(d.x); })
            //.attr("height", function (d) { return y(d.y + d.dy) - y(d.y); });
    }
};

main();
