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
function computeEstimationRows(id){
  /*
   * Compute Estimation line total
   */
  var totalinput = $("#total_" + id + " .input");
  var price = $("#price_" + id + " input")[0].value;
  var quantity = $("#quantity_" + id + " input")[0].value;
  var total = transformToCents(price) * transformToCents(quantity);
  totalinput.empty().html( formatAmount(total) );
}
function computeRowsTotal(){
  /*
   * Compute the estimation Total
   * and subtotals
   */
  var sum = 0;
  $("div.linetotal .input").each(function(){
    sum += transformToCents($(this).text());
  });
  return sum;
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
  price = Math.round(price*100) / 100;
  price = String(price);
  var splitted = price.split('.');
  if (splitted[1] != undefined){
    var cents = splitted[1];
    if (cents.length===1){
      cents += '0';
    }
  }else{
    cents = '00';
  }
  return splitted[0] + "," + cents;
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
  var linestotal = computeRowsTotal();
  var discount = getDiscount();
  var HTTotal = linestotal - discount;
  var tva = getTVA();
  var tvaPart = getTvaPart( HTTotal, tva );
  var expenses = getExpenses();
  var total = HTTotal + tvaPart + expenses;
  $('#linestotal .input').empty().html(formatAmount(linestotal));
  $('#httotal .input').empty().html(formatAmount(HTTotal));
  $('#tvapart .input').empty().html(formatAmount(tvaPart));
  $('#total .input').empty().html(formatAmount(total));
  updatePayments(total);
  return total;
}
function computePaymentRows(){
  /*
   * Return the sum of manually configured values in the payment lines
   */
  console.log("** computePaymentRows");
  var sum = 0;
  $(".paymentamount input").each(function(){
    sum += transformToCents($(this).val());
  });
  console.log("  -> %s", sum);
  console.log("-------------");
  return sum;
}
function updatePayments(total){
  /*
   * Update the payments lines
   * Needed to allow manual configuration
   */
  if (total === undefined){
    total = transformToCents($('#total .input').text());
  }
  var nbpayments = getNbPayments();
  if (nbpayments === -1){
    // Manual payment
    var topay = setAccount(total);
    var linesum = computePaymentRows();
    var rest = topay - linesum;
    $('.paymentamount .input').html(formatAmount(rest));
  }else{
    // Computed payments
    setPaymentValues(total, nbpayments);
  }
}
function setAccount(total){
  /*
   * Compute and set the account line (if needed)
   */
  console.log("** setAccount");
  var account_percent = getAccountPercent();
  var account_amount = setAccountAmount(total, account_percent);
  var topay = total - account_amount;
  console.log("Rest to be paid : %s", topay);
  return topay;
}
function setPaymentValues(total, nbpayments){
  /*
   * Compute and set the payment amounts
   */
  $("#paymentcontainer").empty();
  if (total === undefined){
    total = transformToCents($('#total .input').text());
  }
  if (nbpayments === undefined){
    nbpayments = getNbPayments();
  }
  var topay = setAccount(total);
  if (nbpayments === -1){
    // we ask for manual payment configuration
    // we want two lines (one manually configured,
    //  one fitting the total value)
    setDividedPayments(topay, 2, false);
  }else{
    setDividedPayments(topay, nbpayments);
  }
  return total;
}
function setDividedPayments(total, nbpayments, readonly){
  /*
   *  build and fill divided payments interface
   *  @total : rest to be paied after amount substitution
   *  @nbpayments : number of payments we need to propose
   */
  if (readonly === undefined){
    readonly = true;
  }
  var description = 'Livrable';
  var part = 0;
  if(nbpayments > 1){
    // When we divide the payments, we need to compute the part
    var p = total * 100 / nbpayments;
    part = Math.round( p / 100 );
  }
  // Rest is equal to total if nbpayments <=1
  var rest = total - ( (nbpayments-1) * part );

  for (i=1; i< nbpayments; i++){
    addPaymentRow({id:i,
                    amount:formatAmount(part),
                    readonly:readonly,
                    description:description});
    description = "Paiement " + (i+1);
  }
  addPaymentRow({id:nbpayments,
                  amount:formatAmount(rest),
                  readonly:true,
                  description:description});
}
function addPaymentRow(args, after){
  /*
   * Add a payment line
   */
  if (args === undefined){
    args = new Object();
  }
  if (args['id'] === undefined){
    var id = getNextId("div.paymentline", "paymentline_");
    args['id'] = id;
  }
  var line = getPaymentRow(args);
  if (after === undefined){
    $("#paymentcontainer").append(line);
  }else{
    $(after).after(line);
  }
  if (!(args['readonly'])){
    $('#amount_' + args['id']).blur(function(){
      updatePayments();
    });
  }
  console.log("Setting datepicker %s", args['id']);
  $("#paymentDate_" + args['id']).datepicker();
}
function getNbPayments(){
  /*
   * Return the number of configured payments
   */
  return parseInt($("#nbpayment select").val(), 10);
}
function getIdFromTagId(parseStr, tagid){
  /*
   *  Return an id from a tagid
   *  @param: parseStr: string to parse to get the id from the tagid
   *  @param: tagid: id of the tag to parse
   *  getIdFromTagId("abcdefgh_", "abcdefgh_2") => 2
   */
  return parseInt(tagid.substring(parseStr.length), 10);
}
function getNextId(selector, parseStr){
  /*
   * Returns the next available id
   */
  var newid = 1;
  $(selector).each(function(){
    var tagid = this.id;
    var lineid = getIdFromTagId(parseStr, tagid);
    if (lineid >= newid){
      newid = lineid + 1;
    }
  });
  return newid;
}
function getRow(args){
  /*
   * Return html code for an estimation line
   */
  var template = $( '#prestationTmpl' ).template();
  return $.tmpl(  template, args );
}
function addEstimationRow(args){
  /*
   * Add an estimation line
   * @param: args : initialization datas
   */
  if (args === undefined){
    args = new Object();
  }
  var id = getNextId('div.estimationline', "estimationline_");
  args["id"] = id;
  var html = getRow(args);
  $( '#estimationcontainer' ).append(html);
  $("#quantity_" + id + " input").blur(function(){
      computeEstimationRows(id);
      computeTotal();
      });
  $("#price_" + id + " input").blur(function(){
      computeEstimationRows(id);
      computeTotal();
      });
  computeEstimationRows(id);
  computeTotal();
  console.log("Setting focus");
  $("#estimationline_" + id + " textarea").focus();
}
function getPaymentRow(args){
  /*
   *  return a payment line in html format
   *  @param:args: templating datas
   */
  var template = $( '#paymentTmpl' ).template();
  html = $.tmpl(  template, args );
  return html;
}
function transformToCents(value) {
  /*
   * Transform the value to cents
   */
  var cents;
  var centimes;
  var sval = "" + value;
  var i;

  if ((value === undefined)||(value === null)){
    value = "0.00";
  }
  value = value.replace(",", ".");
  result = parseFloat(value);
  if (isNaN(result)){
    return 0.0;
  }else{
    return result;
  }
}
function setDefault(){
  /*
   * initialize the estimation creation form
   */
  addEstimationRow();
  $('#expenses input').blur(function(){
    computeTotal();
  });
  $('#discount input').blur(function(){
    computeTotal();
  });
  $('#tva select').change(function(){
    computeTotal();
  });
  $("#taskDate").datepicker();
  $('#account_percent select').change(function(){
    updatePayments();
  });
  $('#nbpayment select').change(function(){
    setPaymentValues();
  });
  computeTotal();
  setPaymentValues();
}
function getAccountPercent(){
  /*
   * return the amount of account
   */
  console.log("** getAccountPercent");
  var percent = transformToCents($('#account_percent select').val());
  console.log("    -> Percent : %s", percent);
  return percent;
}
function computeAccount(total, percent){
  /*
   *  Compute the expected account
   */
  console.log("** Computing Account total : %s percent : %s", total, percent);
  var result = total * percent / 100;
  console.log("   -> Result : %s", result);
  return result;
}
function setAccountAmount(total, percent){
  /*
   *  set the amount of the account
   *  @total : TTC total
   *  @percent : percent of the account
   */
  var value = computeAccount( total, percent );
  if (percent > 0){
    $("#account_amount .input").html(formatAmount(value));
    $("#account_container").css("display", "table-row");
  }else{
    $("#account_container").hide();
  }
  return value;
}
function delRow(id){
  /*
   * Remove the estimation line of id 'id'
   */
  $('#' + id).remove();
  computeTotal();
}
