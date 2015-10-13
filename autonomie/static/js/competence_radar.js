/*
 * File Name : competence_radar.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 *
 */
var AppOptions = {};
function addLegend(legend_options, config){
  /*
   * Add legends to the chart
   *
   * :param list legend_options: list of labels
   * :param obj config: the config object used to build the chart
   */
  var colorscale = d3.scale.category10();

  var root_svg = d3.select('#radar').selectAll('svg');

  svg = root_svg.append('svg').attr("width", config.w + 300).attr("height", config.h);

  var text = svg.append("text");
  text = text.attr("class", "title");
  text = text.attr('transform', 'translate(90,0)');
  text = text.attr("x", config.w );
  text = text.attr("y", 20);
  text = text.attr("font-size", "16px");
  text = text.attr("font-weight", "bold");
  text = text.attr("fill", "#404040");
  text = text.text("Échéance d'évaluation");

  var legend = svg.append("g");
  legend = legend.attr("class", "legend");
  legend = legend.attr("height", 100);
  legend = legend.attr("width", 200);
  legend = legend.attr('transform', 'translate(120,20)');

  legend.selectAll('rect').
    data(legend_options).
    enter().
    append("rect").
    attr("x", config.w + 5).
    attr("y", function(d, i){ return i * 30 + 20;}).
    attr("width", 20).
    attr("height", 20).
    style("fill", function(d, i){ return colorscale(i);}).
    on('mouseover', function (d, i){
      z = "polygon.radar-chart-serie" + i;
      root_svg.selectAll("polygon").transition(200).style("fill-opacity", 0.1);
      root_svg.selectAll(z).transition(200).style("fill-opacity", 0.7);
      document.body.style.cursor = 'pointer';
    }).
    on('mouseout', function(){
      root_svg.selectAll("polygon").
        transition(200).
        style("fill-opacity", config.opacityArea);
      document.body.style.cursor = '';
		});
  //Create text next to squares
  legend.selectAll('text').
    data(legend_options).
    enter().
    append("text").
    attr("x", config.w + 38).
    attr("y", function(d, i){ return i * 30 + 15 + 20;}).
    attr("font-size", "14px").
    text(function(d) { return d; }).
    on('mouseover', function (d, i){
      z = "polygon.radar-chart-serie" + i;
      root_svg.selectAll("polygon").transition(200).style("fill-opacity", 0.1);
      root_svg.selectAll(z).transition(200).style("fill-opacity", 0.7);
      document.body.style.cursor = 'pointer';
    }).
    on('mouseout', function(){
      root_svg.selectAll("polygon").
        transition(200).
        style("fill-opacity", config.opacityArea);
      document.body.style.cursor = '';
		});
}
$(function(){
  if (AppOptions['loadurl'] !== undefined){

    var radar_config = {
      w: 400,
      h: 400,
      width: 500,
      height: 350,
      opacityArea: 0.3,
      ExtraWidthX: 600
    };

    var datas_load = initLoad(AppOptions['loadurl']).then(
      function(result){
        var config = _.extend(radar_config, result.config);
        console.log(config);
        RadarChart.draw("#radar", result.datas, config);
        addLegend(result.legend, radar_config);
      }
    );
  }
});
