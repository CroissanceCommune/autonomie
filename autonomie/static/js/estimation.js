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
  var totalinput = $("#total_" + id + " input");
  var price = $("#price_" + id + " input")[0].value;
  var quantity = $("#quantity_" + id + " input")[0].value;
  var total = transformToCents(price) * transformToCents(quantity);
  console.log("total : %s", total);
  console.log(totalinput);
  totalinput.val( formatAmount(total) );
}
function computeLinesTotal(){
  /*
   * Compute the estimation Total
   * and subtotals
   */
  var linestotal = 0;
  $("div.linetotal input").each(function(){
    linestotal += transformToCents($(this).html());
  });
  return linestotal;
}
function getDiscount(){
  /*
   * Returns the current discount
   */
  return transformToCents($("#discount input").val());
}
function getTVA(){
  /*
   *  Returns the current tva
   */
  var tva = $("#tva select").val();
  if (tva <0){
    tva = 0;
  }
  return tva;
}
function getTvaPart(total, tva){
  /*
   * returns the value of the tva
   */
  return total * (tva / 10000);
}
function getExpenses(){
  /*
   *  Return the current expense configured
   */
  return transformToCents( $('#expenses input').val() );
}
function formatPrice(price) {
  /*
   * Return a formatted price
   * @price : compute-formatted price
   */
  var cents = $.trim("" + price);
  var idx = cents.indexOf(".");
  var centimes;
  if(idx >= 0) {
    if(Math.round("0." + cents.substring(idx + 1)) > 0)
      price ++;
    cents = $.trim("" + price);
    idx = cents.indexOf(".");
    cents = cents.substring(0, idx);
  }

  centimes = cents.substring(cents.length - 2);
  if(centimes.length === 0)
    centimes = "00";
  else if(centimes.length < 2)
    centimes = "0" + centimes;
  return Math.floor(price / 100) + "," + centimes;
}
function formatAmount( amount ){
  /*
   * return a formatted user-friendly amount
   */
  return formatPrice( amount ) + "&nbsp;&euro;";
}
function computeTotal(){
  /*
   * Compute the main totals
   */
  console.log("Computing the total");
  var linestotal = computeLinesTotal();
  var discount = getDiscount();
  var HTTotal = linestotal - discount;
  var tva = getTVA();
  var tvaPart = getTvaPart( HTTotal, tva );
  var expenses = getExpenses();
  var total = HTTotal + tvaPart + expenses;
  console.log("Linestotal : %s", linestotal);
  console.log("discount: %s", discount);
  console.log("HTTotal: %s", HTTotal);
  console.log("tva : %s", tva);
  console.log("tvaPart : %s", tvaPart);
  console.log("expenses : %s", expenses);
  console.log("total : %s", total);
  $('#linestotal input').empty().html(formatAmount(linestotal));
  $('#httotal input').empty().html(formatAmount(HTTotal));
  $('#tvapart input').empty().html(formatAmount(tvaPart));
  $('#total input').empty().html(formatAmount(total));
}
function getNextId(){
  /*
   * Returns the next available id
   */
  var newid = 1;
  $('div.estimation_line').each(function(){
    var lineid = parseInt(this.id.substring("estimation_line_".length), 10);
    if (lineid >= newid){
      newid = lineid + 1;
    }
  });
  return newid;
}
function addLine(){
  /*
   * Add an estimation line
   */
  var template = $( '#prestationTmpl' ).template();
  var id = getNextId();
  args = { id : id };
  html = $.tmpl(  template, args );
  console.log(html);
  $( '#estimationcontainer' ).append(html);
  $("#quantity_" + id + " input").blur(function(){
      computeLineTotal(id);
      computeTotal();
      });
  $("#price_" + id + " input").blur(function(){
      computeLineTotal(id);
      computeTotal();
      });
}
function transformToCents(value) {
  /*
   * Transform the value to cents
   */
  var cents;
  var centimes;
  var sval = "" + value;
  var i;

  i = sval.indexOf('.');
  if(i < 0)
    i = sval.indexOf(',');

  if(i >= 0) {
    centimes = sval.substr(i + 1, 2);
    if(centimes.length < 1)
      centimes = "00";
    else if(centimes.length < 2)
      centimes = centimes + "0";
    cents = sval.substr(0, i) + centimes;
  }
  else {
    cents = value * 100;
  }

  return cents;
}
function setDefault(){
  /*
   * initialize the estimation creation form
   */
  addLine();
  $('#expenses input').blur(function(){
    computeTotal();
  });
  $('#discount input').blur(function(){
    computeTotal();
  });
  $('#tva select').change(function(){
    computeTotal();
  });
}
