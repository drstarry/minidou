function drawChart() {
  var container = $(".influence-graph").html('');

  var margin = {left: 40, right: 40, top: 20, bottom: 30},
      width = container.innerWidth() - margin.left - margin.right,
      height = container.innerHeight() - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y").parse;

  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);

  var xAxis = d3.svg.axis().scale(x).orient("bottom");
  var yAxis = d3.svg.axis().scale(y).orient("left");

  var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    //.y0(height)
    .y(function(d) { return y(d.value); });

  var svg = d3.select(container[0]).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.json("influence/trends", function(error, data) {
    data.forEach(function(d) {
	  d.year=d.date;
      d.date = parseDate(d.date);
      d.value = +d.value;
	  d.pap1=d.pap1;
	  d.au1=d.au1;
	  d.cit1=d.cit1;
	  d.pap2=d.pap2;
	  d.au2=d.au2;
	  d.cit2=d.cit2;
    });

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Influence");
		
	// Draw the points
	dataCirclesGroup = svg.append('svg:g');

	var circles = dataCirclesGroup.selectAll('.data-point')
		.data(data);

	circles
		.enter()
			.append('svg:circle')
				.attr('class', 'data-point')
				.style('opacity', 1e-6)
				.attr('cx', function(d) { return x(d.date) })
				.attr('cy', function() { return y(0) })
				.attr('r', function() { return (data.length <= 50) ? 4 : 0 })
			.transition()
			.duration(1000)
				.style('opacity', 1)
				.attr('cx', function(d) { return x(d.date) })
				.attr('cy', function(d) { return y(d.value) });

	circles
		.transition()
		.duration(1000)
			.attr('cx', function(d) { return x(d.date) })
			.attr('cy', function(d) { return y(d.value) })
			.attr('r', function() { return (data.length <= 50) ? 4 : 0 })
			.style('opacity', 1);

	circles
		.exit()
			.transition()
			.duration(1000)
				.attr('cy', function() { return y(0) })
				.style("opacity", 1e-6)
				.remove();	
	
	$('svg circle').hover(function() {
	  var d = this.__data__;
	  var html;
	  if (d.pap2!=0){
	    html = '<span class="title">' + d.pap1 +'<br></span><span class="author">'+d.au1 + ' </span><br>'+d.year+'<span class="cita">CitedBy: ' + d.cit1
		  +'</span><br><span class="title"><br>' + d.pap2  +'<br></span><span class="author">'+d.au2 +'</span><br> '+d.year+'<span class="cita">CitedBy: ' 
		  + d.cit2 +"</span>";
	  } else {
	    html = '<span class="title">' + d.pap1+'<br></span><span class="author">'+d.au1 + ' </span><br>'+d.year+'<span class="cita">Citations: ' + d.cit1;
	  }
	  $('.detailed-info').html(html);
        });
  });
};

function drawPie() {
  var container = $(".influence-pie").html('');
  var w = container.innerWidth();
      h = container.innerHeight();
      r = Math.min(w, h) / 2;
  color = d3.scale.category20c();

d3.json("influence/paper", function(error, json) {
  if (error) return console.warn(error);
  data = json;
  var vis = d3.select(container[0])
      .append("svg:svg")
      .data([data])
          .attr("width", w)
          .attr("height", h)
      .append("svg:g")
          .attr("transform", "translate(" + r + "," + r + ")")

  var arc = d3.svg.arc()
      .outerRadius(r);

  var pie = d3.layout.pie().value(function(d) { return d.value; });

  var arcs = vis.selectAll("g.slice")
      .data(pie)
      .enter()
          .append("svg:g")
              .attr("class", "slice");

      arcs.append("svg:path")
              .attr("fill", function(d, i) { return color(i); } )
              .attr("d", arc);

      arcs.append("svg:text")
          .attr("transform", function(d) {
              d.innerRadius = 0;
              d.outerRadius = r;
              return "translate(" + arc.centroid(d) + ")";
          })
          .attr("text-anchor", "middle")
          .text(function(d, i) { return data[i].label; });
});  
};

function drawTable() {
d3.json("influence/miserable", function(miserables) {
  var index;
  for (index=0;index<5;index++){
  
  var margin = {top: 120, right: 0, bottom: 10, left: 140},
    width = 300,
    height = 300;

var x = d3.scale.ordinal().rangeBands([0, width]),
    z = d3.scale.linear().domain([0, 4]).clamp(true),
    c = d3.scale.category10().domain(d3.range(10));

var svg = d3.select(".topic-analysis.index" + index + " .table").append("svg")//".topic-analysis.index" + index + " .table"
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
  var matrix = [],
      nodes = miserables[index].nodes
      n = nodes.length;

  // Compute index per node.
  nodes.forEach(function(node, i) {
    node.index = i;
   // node.count = 0;
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
  });

  // Convert links to matrix; count character occurrences.
  miserables[index].links.forEach(function(link) {
    //alert(link.value);
      matrix[link.source][link.target].z += link.value;
   // nodes[link.source].count += link.value;
   // nodes[link.target].count += link.value;
  });

  // Precompute the orders.
  var orders = {
    name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
    //count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
  //  group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
  };

  // The default sort order.
  x.domain(orders.name);

  svg.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height)
	  .attr("fill","white");

  var row1 = svg.selectAll(".row")
      .data(matrix)
    .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row);

  row1.append("line")
      .attr("x2", width);

  row1.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return nodes[i].name; });

  var column = svg.selectAll(".column")
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column.append("line")
      .attr("x1", -width);

  column.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .text(function(d, i) { return nodes[i].name; });
}
  function row(row) {
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z; }))
      .enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return d.z; })
        //.style("fill", function(d) { return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null; })
		.style("fill","red")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);
  }

  function mouseover(p) {
    d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll("text").classed("active", false);
  }

  function order(value) {
    x.domain(orders[value]);

    var t = svg.transition().duration(2500);

    t.selectAll(".row")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .selectAll(".cell")
        .delay(function(d) { return x(d.x) * 4; })
        .attr("x", function(d) { return x(d.x); });

    t.selectAll(".column")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
  }
});

}
!function() {
  $('.topics').on('click', '.topic-list li', function() {
    if ($(this).hasClass('active')) return;
	//drawTable();
    var index = $(this).data('index');
    $('.topic-analysis:visible').hide();
    $('.topic-analysis.index' + index).fadeIn();
    $(this).siblings().removeClass('active');
    $(this).addClass('active');
  });
}();

!function() {
  $(window).resize(function() {
    //drawPie();
    drawChart();
    $('.entity-img').one('load', function() {
      $('.entity-img').css('top', $('.entity-img').parent().parent().innerHeight() / 2 - $('.entity-img').outerHeight() / 2);
    }).one('error', function() {
      $(this).attr('src', 'http://static02.linkedin.com/scds/common/u/img/icon/icon_no_company_logo_100x60.png');
    });
  }).trigger('resize');
  $('.topics').load('influence/topics/latest', function() {
    $('.topic-list li:nth(0)').click();
	drawPie();
	drawTable();
  });
}();
