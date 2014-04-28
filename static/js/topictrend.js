$(".navbar-inner").append('<div class="form-search pull-right"><input type="text" class="input-medium search-query"' +
	' id="topic-trend-search-text"><button class="btn" id="topic-trend-search">Search</button></div>');

var margin = {
	top: 1,
	right: 1,
	bottom: 6,
	left: 1
},
	width = $(window).width() - 240 - margin.left - margin.right,
	height = 1050 - margin.top - margin.bottom;

var formatNumber = d3.format(",.0f"),
	format = function(d) {
		return formatNumber(d) + " TWh";
	},
	color = d3.scale.category20();

var chart = d3.select("#chart").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)


var sankey = d3.sankey()
	.nodeWidth(0)
	.nodePadding(15)
	.size([width, 300]);

var path = sankey.link();

var area = d3.svg.area()
	.x(function(d) {
		return d.x;
	})
	.y0(function(d) {
		return d.y0;
	})
	.y1(function(d) {
		return d.y1;
	});

var y = d3.scale.linear()
	.range([height, 0]);

$("#chart").on({
	ajaxStart: function() {
		$(this).addClass("loading");
	},
	ajaxStop: function() {
		$(this).removeClass("loading");
	}
});

chart.append("line").attr("x1", 0).attr("x2", width).attr("y1", 350).attr("y2", 350).style("stroke", "darkgray").style("stroke-width", 1);

d3.select("#topic-trend-search").on("click", function(e) {
	render_topic($("#topic-trend-search-text").val(), 0, 10000); // parseInt($("#topic-trend-search-start").val()), parseInt($("#topic-trend-search-end").val()), parseInt($("#topic-trend-search-timewindow").val()));
})

$(document).ready(function() {
	var get_query = function(name) {
		name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
		var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
			results = regex.exec(location.search);
		return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
	};
	var query = get_query('q');
	if (query.length > 0) {
		render_topic(query, 0, 10000);
	}
});

var timeline = d3.select("#right-box").append("svg");
var bar_pos = 170;
var timeline_item_offset = 20;
var ball_radius = 6;
var hist_height = 100;
// function resize_chart(){
//   d3.select("#chart").style("width", (window.width - 2 * 50)+"px");
// }

// resize_chart();
// window.onresize = resize_chart();
// render_topic("deep learning", 0, 10000);
// document.getElementById("topic-trend-search-text").value ="deep learning";
// document.getElementById("topic-trend-search-threshold").value =0.0001;

function render_topic(q, start, end) {
	chart.remove();
	chart = d3.select("#chart").append("svg").attr("width", width) //width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	svg = chart.append("g")
		.attr("height", 350)
		.attr("id", "trend");

	chart.append("line").attr("x1", 0).attr("x2", width).attr("y1", 330).attr("y2", 330)
		.style("stroke", "darkgray").style("stroke-width", 1);

	timeline.remove();
	timeline = d3.select("#right-box").append("svg");

	$("#chart").addClass("loading");

	
	d3.json("terms?q=" + q + "&start=" + start + "&end=" + end, function(energy) {
		$("#chart").removeClass("loading");
		//data transformation
		var terms = {};
		max_sum = 0;
		energy.terms.forEach(function(t) {
			t.sum = 0;
			//wangxiao
			t.year.forEach(function(tt){
				if ((tt.y>2010)&&(tt.d>0)) {
					t.sum+=tt.d;
				}
			});
			if (t.sum > max_sum) {
				max_sum = t.sum;
			};
			terms[t.t] = t;
		})

		var people = {};
		energy.people.forEach(function(t) {
			people[t.id] = t;
		})

		timeline.attr("height", function(d) {
			return 25 * energy.terms.length;
		})

		//right box, hist diagram
		timeline.append("line")
			.attr("x1", bar_pos + 10)
			.attr("x2", bar_pos + 10)
			.attr("y1", 0)
			.attr("y2", function(){
				return 25 * energy.terms.length;
			})
			.style("stroke", "gray")
			.style("stroke-width", .5);

		max_freq = 0;
		energy.terms.forEach(function(d) {
			if (d.freq > max_freq) {
				max_freq = d.freq;
			}
		});
//flagD
		d3.select("#nav").style("display","");
		d3.select(".active").classed("active",false);
		d3.select($("#first-three").parent()[0]).classed("active","true");
		
		function draw_right_box(){
			energy.terms.sort(function(a,b){return b.sum-a.sum})
			var hist =
			timeline.append("g")
			.selectAll(".term")
			.data(energy.terms)
			.enter()
			.append("g")
			.attr("class", "term")
			.attr("transform", function(d, i) {
				return "translate(" + [0, i * timeline_item_offset + 20] + ")rotate(" + 0 + ")";
			})
			.attr("id", function(d){
				return "term-"+d.idx;
			})
			.on("click", function(d) {
				draw_flow(d);
			})

			hist.append("rect")
				.attr("x", function(d) {
					return bar_pos + 10;
				})
				.attr("y", function(d) {
					return 0;
				})
				.attr("height", 18)
				.attr("width", function(d) {
					return hist_height * d.sum / max_sum;
				})
				.style("fill-opacity", 0.7)
				.style("fill", "#60aFe9")
				.append("svg:title")
				.text(function(d) { return d.sum; });
	
			hist.append("text")
				.attr("text-anchor", "end")
				.attr("transform", function(d) {
					return "translate(" + [bar_pos, 0] + ")rotate(" + 0 + ")";
				})
				.style("font-size", 12)
				.attr("dy", ".85em")
				.text(function(d) {
					return d.t;
				})
		}
		draw_right_box();
		d3.select("#first-three").on("click", function(e){
			d3.select(".active").classed("active",false);
			d3.select(this.parentNode).classed("active",true);
			d3.selectAll(".term").remove();
			energy.terms.sort(function(a,b){return b.freq-a.freq});
			draw_right_box();
			draw_flow(terms[q]);
		})
//flag
		d3.select("#revert").on("click", function(e) {
			d3.select(".active").classed("active",false);
			d3.select(this.parentNode).classed("active","true");
			d3.selectAll(".term").remove();
			energy.terms.sort(function(a,b){return b.freq-a.freq})

			var hist =
				timeline.append("g")
				.selectAll(".term")
				.data(energy.terms)
				.enter()
				.append("g")
				.attr("class", "term")
				.attr("id", function(d){
					return "term-"+d.idx;
				})
				.attr("transform", function(d, i) {
					return "translate(" + [0, i * timeline_item_offset + 20] + ")rotate(" + 0 + ")";
			})
			.on("click", function(d) {
				draw_flow(d);
			})
			
			hist.append("rect")
				.attr("x", function(d) {
					return bar_pos + 10;
				})
				.attr("y", function(d) {
					return 0;
				})
				.attr("height", 18)
				.attr("width", function(d) {
					return hist_height * d.freq / max_freq;
				})
				.style("fill-opacity", 0.7)
				.style("fill", "#60aFe9")
				.append("svg:title")
				.text(function(d) { return d.sum; });

			hist.append("text")
				.attr("text-anchor", "end")
				.attr("transform", function(d) {
					return "translate(" + [bar_pos, 0] + ")rotate(" + 0 + ")";
				})
				.style("font-size", 12)
				.attr("dy", ".85em")
				.text(function(d) {
					return d.t;
				})
			draw_flow(terms[q]);
		})

		var time_slides_dict = {};
		var time_slides_offset = {};
		energy.time_slides.forEach(function(time, i) {
			time.sort();
			time.forEach(function(year, j) {
				time_slides_dict[year] = i;
				time_slides_offset[year] = j;
			})
		})

		var time_window = energy.time_slides[0].length;

		var x = function(year) {
			return (time_slides_dict[year] + ((1 / time_window) * time_slides_offset[year])) * width / energy.time_slides.length;
		}

		var axis = svg.append("g").selectAll(".axis")
			.data(energy.time_slides)
			.enter().append("g")
			.attr("class", "axis")
			.attr("transform", function(d, i) {
				return "translate(" + (i) * width / energy.time_slides.length + "," + 0 + ")";
			})

		axis.append("line")
			.attr("x1", function(d) {
				return 0;
			})
			.attr("x2", function(d) {
				return 0;
			})
			.attr("y1", function(d) {
				return 0;
			})
			.attr("y2", function(d) {
				return 1000;
			})
			.style("stroke", function(d) {
				return "lightgray";
			})
			.style("stroke-width", function(d) {
				return 1;
			})

		axis.append("text")
			.attr("x", -6)
			.attr("y", 10)
			.attr("dy", ".0em")
			.attr("text-anchor", "end")
			.attr("transform", null)
			.text(function(d, i) {
				return d3.min(d);
			})
			.attr("x", 6)
			.attr("text-anchor", "start")
			.style("font-weight", "bold");

		sankey
			.nodes(energy.nodes)
			.links(energy.links)
			.items(energy.terms)
			.nodeOffset(width / energy.time_slides.length)
			.layout(32);

		var link = svg.append("g").selectAll(".link")
			.data(energy.links)
			.enter().append("path")
			.attr("class", "link")
			.attr("d", path)
			.style("stroke-width", function(d) {
				return 20
			})
			.style("fill-opacity", .6)
			.style("fill", function(d) {
				var key = "gradient-" + d.source_index + "-" + d.target_index;
				svg.append("linearGradient")
					.attr("id", key)
					.attr("gradientUnits", "userSpaceOnUse")
					.attr("x1", d.source.x + 50).attr("y1", 0)
					.attr("x2", d.target.x).attr("y2", 0)
					.selectAll("stop")
					.data([{
						offset: "0%",
						color: color(d.source.cluster)
					}, {
						offset: "100%",
						color: color(d.target.cluster)
					}])
					.enter().append("stop")
					.attr("offset", function(d) {
						return d.offset;
					})
					.attr("stop-color", function(d) {
						return d.color;
					});
				return d.color = "url(#" + key + ")";
			})
			.sort(function(a, b) {
				return b.dy - a.dy;
			});

		link.append("title")
			.text(function(d) {
				return d.source.name + " → " + d.target.name;
			});

		var node = svg.append("g").selectAll(".node")
			.data(energy.nodes)
			.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) {
				return "translate(" + d.x + "," + d.y + ")";
			})
			.call(d3.behavior.drag()
				.origin(function(d) {
					return d;
				})
				.on("dragstart", function() {
					this.parentNode.appendChild(this);
				})
				.on("drag", dragmove));

		node.append("rect")
			.attr("height", function(d) {
				return d.dy;
			})
			.attr("width", sankey.nodeWidth())
			.style("fill", function(d) {
				return d.color = color(d.cluster);
			})
			.style("stroke", function(d) {
				return d.color;
			}) //d3.rgb(d.color).darker(2); })
			.style("stroke-width", function(d) {
				return 0;
			})
			.style("opacity", function(d) {
				return 0.6;
			})
			.append("title")
			.text(function(d) {
				return d.name + "\n" + format(d.value);
			});

		node.append("text")
			.attr("x", -20)
			.attr("y", function(d) {
				return d.dy / 2;
			})
			.attr("text-anchor", "middle")
			.attr("transform", null)
			.text(function(d) {
				return d.name;
			})
			.style("fill", function(d) {
				return "black" //color(d.cluster);
			})
			.style("font-weight", "bold")
			.style("font", function(d) {
				var w = d.w;
				if (w > 15) {
					w = 15;
				}
				if (w < 10 && w > 0) {
					w = 10;
				}
				return (w) + "px sans-serif";
			});


		energy.terms.sort(function(a, b) {
			return b.start.year - a.start.year;
		})

		var item = svg.append("g").selectAll(".item")
			.data(energy.terms)
			.enter().append("g")
			.attr("class", "item")
			.attr("transform", function(d) {
				return "translate(" + x(d.start.year) + "," + (d.start.node.y + d.start.node.dy / 2) + ")";
			});

		item.append("circle")
			.attr("cx", function(d) {
				return 0;
			})
			.attr("cy", function(d) {
				return 0;
			})
			.attr("r", function(d) {
				return d.freq / 10;
			})
			.style("stroke-width", 1)
			.style("stroke", function(d) {
				return color(d.start.cluster);
			})
			.style("stroke-opacity", .5)
			.style("fill", function(d) {
				return color(d.start.cluster);
			})
			.style("display", "none");

		var basis = d3.svg.area()
			.x(function(d, i) {
				return x(d.y)
			})
			.y0(function(d) {
				if (d.d < 30)
					return 200 - (d.d) * 5;
				return 50
			})
			.y1(function(d) {
				if (d.d < 30)
					return 200 + d.d * 5;
				return 350
			})
			.interpolate("basis");

		var flow = chart
			.append("g")
			.attr("transform", function(d) {
				return "translate(" + [0, 350] + ")rotate(" + 0 + ")";
			})

		var draw_flow = function(data) {
			flow.remove();
			flow = chart.append("g")
				.attr("transform", function(d) {
					return "translate(" + [0, 350] + ")rotate(" + 0 + ")";
				});

			d3.select(".strong").remove()
			d3.select("#term-"+data.idx)
				.append("rect")
				.attr("class","strong")
				.attr("x","0px")
				.attr("y", function(d){
					return -1.8125;
				})
				.attr("width", "300px")
				.attr("height",  function(d){
					return 19.8125;
				})
				.style("fill","#9900FF")
				.style("fill-opacity", 0.2);


			flow.append("path")
				.attr("d", function(d) {
					return basis(data.year);
				})
				.style("stroke-width", 0.2)
				.style("stroke", "#60afe9")
				.style("fill", "#60afe9")

			var count = 0;
			var people_flow = d3.layout.force()
				.linkDistance(80)
				.charge(-120)
				.gravity(.05)
				.size([])

			var channels=[]
			for(var i=0; i<40; i++){
				channels[i] = [];
			}
			var people_flow = flow.append("g").selectAll(".people")
				.data(data.first.sort(function(a,b){
					return a.y - b.y
				}))
				.enter()
				.append("g")
				.attr("class", "people")
				.attr("transform", function(d, i) {
					var c = 0
					for(var i = 0; i < 40; i++){
						if(channels[i].length > 0){
							if(d.y - d3.max(channels[i]) < 4){
								continue;
							}
						}
						channels[i].push(d.y);
						break;
					}
					if(i%2 == 0){
						return "translate(" + [x(d.y), 200 -i/2 * 12] + ")rotate(" + 0 + ")";
					}else{
						return "translate(" + [x(d.y), 200 +(i+1)/2 * 12] + ")rotate(" + 0 + ")";
					}
					
				});
			people_flow.append("text")
				.attr("text-anchor", "end")
				.style("font-size", 10)
				.attr("dy", ".85em")
				.attr("transform", function(d) {
					return "translate(" + [-5, -5] + ")rotate(" + 0 + ")";
				})
				.text(function(d) {
					return people[d.p].name;
				});
			people_flow.append("circle")
				.attr("cx", 0)
				.attr("cy", 0)
				.attr("r", 5)
				.style("stroke-width", 1)
				.style("stroke", function(d) {
					return "#eee";
				})
				.style("opacity", .8)
				.style("fill", function(d) {
					return "orangered";
				})
		}

		draw_flow(terms[q]);


		function dragmove(d) {
			d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
			sankey.relayout();
			link.attr("d", path);
		}

		var leftPos = $('#chart').scrollLeft();
		$("#chart").animate({
			scrollLeft: leftPos + 200
		}, 800);
	});
}
