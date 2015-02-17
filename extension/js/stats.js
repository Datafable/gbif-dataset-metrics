var main = function () {
    var datasetKey = getDatasetKeyFromURL();
    addAboveContent();
    getMetrics(datasetKey,addMetricsToStatsPage);
};

var addMetricsToStatsPage = function (metrics) {
    var html = "";
    var anchor = $("#occmetrics");

    // Add bar metrics
    html = html + '<h3>Basis of record</h3>' + basisOfRecordBar(metrics); // Basis of record
    html = html + '<h3>Coordinates</h3>' + coordinatesBar(metrics); // Coordinates
    html = html + '<h3>Multimedia</h3>' + multimediaBar(metrics); // Multimedia
    html = html + '<h3>Taxon match</h3>' + taxonMatchBar(metrics); // Taxon match
    anchor.find(".pies").remove(); // Remove some default elements
    anchor.find(".fullwidth").append(html); // Add new metrics
    
    // Activate bar metrics tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // Add taxonomy partition
    html =  '<article id="taxonomy">' +
                '<header></header>' +
                '<div class="content">' +
                    '<div class="header"><div class="left"><h2>Taxonomy</h2></div></div>' +
                    '<div class="fullwidth" id="taxonomyPartition"></div>' +
                '</div>' +
                '<footer></footer>' +
            '</article>';
    anchor.after(html);
    taxonomyPartition(metrics);
};

var taxonomyPartition = function (metrics) {
    // Based on http://mbostock.github.io/d3/talk/20111018/partition.html
    var width = 874,
        height = 500,
        x = d3.scale.linear().range([0, width]),
        y = d3.scale.linear().range([0, height]);

    var svg = d3.select("#taxonomyPartition")
        .style("height", height + "px")
        .append("svg:svg")
        .attr("width", width)
        .attr("height", height);

    var partition = d3.layout.partition()
        .value(function(d) { return d.size; });

    var root = JSON.parse(metrics.taxonomy);
        data = partition.nodes(root);

    var g = svg.selectAll("g")
        .data(data)
        .enter().append("svg:g")
        .attr("transform", function (d) { return "translate(" + x(d.y) + "," + y(d.x) + ")"; })
        .on("click", click);

    var kx = width / root.dx, // Available width
        ky = height / 1;

    g.append("svg:rect")
        .attr("width", root.dy * kx)
        .attr("height", function(d) { return d.dx * ky; })
        .classed({
            "parent": function(d) { return d.children; },
            "child": function(d) { return !d.children; },
            "unknown": function(d) { return d.name === "Unknown"; }
        });

    g.append("svg:text")
        .attr("transform", transform)
        .attr("dy", ".35em")
        .style("opacity", function(d) { return d.dx * ky > 12 ? 1 : 0; })
        .text(function(d) { return d.size ? d.name + " (" + d.size + ")" : d.name; });

    d3.select(window)
        .on("click", function() { click(root); });

    function click(d) {
        if (!d.children) return;

        kx = (d.y ? width - 40 : width) / (1 - d.y);
        ky = height / d.dx;
        x.domain([d.y, 1]).range([d.y ? 40 : 0, width]);
        y.domain([d.x, d.x + d.dx]);

        var t = g.transition()
            .duration(d3.event.altKey ? 7500 : 750)
            .attr("transform", function(d) { return "translate(" + x(d.y) + "," + y(d.x) + ")"; });

        t.select("rect")
            .attr("width", d.dy * kx)
            .attr("height", function(d) { return d.dx * ky; });

        t.select("text")
            .attr("transform", transform)
            .style("opacity", function(d) { return d.dx * ky > 12 ? 1 : 0; });

        d3.event.stopPropagation();
    }

    function transform(d) {
        return "translate(8," + d.dx * ky / 2 + ")";
    }
};

main();
