/*
 * File Name :
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
function computeLineTotal(id){
  /*
   * Compute Estimation line total
   */
  console.log("Computing line total");
  var totaldiv = $("#total_" + id);
  var price = $("#price_" + id)[0].value;
  var quantity = $("#quantity_" + id)[0].value;
  var total = parseInt(price) * parseInt(quantity);
  /* TODO : test Nan value for total and alert user
  */
  totaldiv.html("<div>" + total + "</div>");
}
function computeTotal(){
  console.log("Computing the total");
}
function addLine(id){
  /* TODO : add id detection
   * TODO : add computeTotal
   */
  var template = $( '#prestationTmpl' ).template();
  args = {id:id};
  html = $.tmpl(  template, args );
  console.log(html);
  $( '#estimationcontainer' ).html(html);
   $("#quantity_" + id).blur(function(){computeLineTotal(id);});
   $("#price_" + id).blur(function(){computeLineTotal(id);});
}
