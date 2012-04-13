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
var Facade = new Object();
/*
 *
 * Utitilities
 *
 *
 */

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

function delRow(id){
  /*
   * Remove the estimation line of id 'id'
   */
  $('#' + id).remove();
  $(Facade).trigger("linedelete");
}
/*
 *
 * Estimation Lines handling (computing ...)
 *
 */

function computeEstimationRow(tag){
  /*
   * Compute Estimation line total
   */
  var row = $(tag);
  var totalinput = row.find(".linetotal .input");
  var cost = row.find("input[name=cost]").val();
  var quantity = row.find("input[name=quantity]").val();
  var total = transformToCents(cost) * transformToCents(quantity);
  totalinput.empty().html( formatAmount(total) );
}
function computeRowsTotal(){
  /*
   * Compute the estimation Total
   * and subtotals
   */
  console.log('## Computing rows total');
  var sum = 0;
  $("div.linetotal .input").each(function(){
    sum += transformToCents($(this).text());
  });
  console.log("  -> %s", sum);
  return sum;
}
function getDiscount(){
  /*
   * Returns the current discount
   */
  return transformToCents($("input[name=discount]").val());
}
function getTVA(){
  /*
   *  Returns the current tva
   */
  var tva = $("select[name=tva]").val();
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
  return transformToCents( $('input[name=expenses]').val() );
}
function formatPrice(price) {
  /*
   * Return a formatted price for display
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
  console.log(" -Lines total : %s", linestotal);
  var discount = getDiscount();
  console.log(" -Discount : %s", discount);
  var HTTotal = linestotal - discount;
  var tva = getTVA();
  var tvaPart = getTvaPart( HTTotal, tva );
  var expenses = getExpenses();
  var total = HTTotal + tvaPart + expenses;
  $('#linestotal .input').empty().html(formatAmount(linestotal));
  $('#httotal .input').empty().html(formatAmount(HTTotal));
  $('#tvapart .input').empty().html(formatAmount(tvaPart));
  $('#total .input').empty().html(formatAmount(total));
  $(Facade).trigger('totalchanged');
}
/*
 *
 *
 * Payment informations
 *
 *
 */
function computePaymentRows(){
  /*
   * Return the sum of manually configured values in the payment lines
   */
  console.log("** computePaymentRows");
  var sum = 0;
  $(".paymentline input[name=amount]").each(function(){
    sum += transformToCents($(this).val());
  });
  console.log("  -> %s", sum);
  console.log("-------------");
  return sum;
}
//function updatePayments(total){
//  /*
//   * Update the payments lines
//   * Needed to allow manual configuration
//   */
//  if (total === undefined){
//    total = transformToCents($('#total .input').text());
//  }
//  var nbpayments = getNbPayments();
//  if (nbpayments === -1){
//    // Manual payment
//    var topay = setDeposit(total);
//    var linesum = computePaymentRows();
//    var rest = topay - linesum;
//    $('.paymentamount .input').html(formatAmount(rest));
//  }else{
//    // Computed payments
//    setPaymentRows(total, nbpayments);
//  }
//}
//function setDeposit(total){
//  /*
//   * Compute and set the account line (if needed)
//   */
//  console.log("** setDeposit");
//  var account_percent = getDepositPercent();
//  var account_amount = setDepositAmount(total, account_percent);
//  var topay = total - account_amount;
//  console.log("Rest to be paid : %s", topay);
//  return topay;
//}
function setPaymentRows(total, nbpayments){
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
  var topay = getToPayAfterDeposit();
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
  for (i=1; i< nbpayments; i++){
    addPaymentRow({id:i,
                    amount:formatAmount(part),
                    readonly:readonly,
                    description:description});
    description = "Paiement " + (i+1);
  }
  // Rest is equal to total if nbpayments <=1
  var rest = total - ( (nbpayments-1) * part );
  setSoldAmount(rest);
}

function computeSoldAmount(){
  /*
   * Return the sold's amount value
   */
  var topayAfterDeposit = getToPayAfterDeposit();
  var sold = topayAfterDeposit - computePaymentRowSum();
}
function getSoldAmountTag(){
  /*
   * Returns the sold row
   */
  return $('#paymentline_1000 .paymentamount .input');
}
function addPaymentRow(args, after){
  /*
   * Add a payment line
   */
  console.log("Adding a payment row");
  console.log(args);
  if (args === undefined){
    args = new Object();
  }
  if (args['id'] === undefined){
    var id = getNextId("div.paymentline", "paymentline_");
    args['id'] = id;
  }
  if (args['readonly'] === undefined){
    if (getNbPayments()>0){
      args['readonly'] = true;
    }else{
      args['readonly'] = false;
    }
  }
  var line = getPaymentRow(args);
  if (after === undefined){
    $("#paymentcontainer").append(line);
  }else{
    $(after).after(line);
  }
  if (!(args['readonly'])){
    $('#amount_' + args['id']).blur(function(){
      $(Facade).trigger('paymentlinechange');
    });
  }
  $("#paymentDate_" + args['id']).datepicker();
}
function getNbPayments(){
  /*
   * Return the number of configured payments
   */
  return parseInt($("select[name=payment_times]").val(), 10);
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
function getPaymentRow(args){
  /*
   *  return a payment line in html format
   *  @param:args: templating datas
   */
  var template = $( '#paymentTmpl' ).template();
  html = $.tmpl(  template, args );
  return html;
}
function computeDeposit(total, percent){
  /*
   *  Compute the expected account
   */
  console.log("** Computing Deposit total : %s percent : %s", total, percent);
  var result = total * percent / 100;
  console.log("   -> Result : %s", result);
  return result;
}
function setDepositAmount(deposit){
  /*
   *  set the amount of the account
   *  @total : TTC total
   *  @percent : percent of the account
   */
  if (deposit > 0){
    $("#account_amount .input").html(formatAmount(deposit));
    $("#account_container").css("display", "table-row");
  }else{
    $("#account_container").hide();
  }
}
function getToPayAfterDeposit(){
  /*
   *  return the topay value after deposit
   */
  return getTotal() - getDeposit();
}
function getDeposit(){
  /*
   * Return the computed deposit
   */
  return getTotal() * getDepositPercent() / 100;
}
function getDepositPercent(tag){
  /*
   * Return the current configured deposit
   * @tag : the select tag where the deposit is configured
   */
    if (tag === undefined){
      tag = 'select[name=deposit]';
    }
    var deposit =  $(tag).val();
    return transformToCents(deposit);
}
function getTotal(){
  /*
   * Return the current total
   */
  return transformToCents($('#total .input').text());
}
function setDeposit(){
  /*
   *  Define the deposit
   *  @percent : deposit percent
   */
  var deposit = getDeposit();
  setDepositAmount(deposit);
}
function setSoldAmount(value){
  /*
   * Set the sold amount
   */
  getSoldAmountTag().html(formatAmount(value));
}
function updatePaymentRows(){
  /*
   * Update payment rows
   */
  var nbpayments = getNbPayments();
  if (nbpayments === -1){
    updateSoldAmount();
  }else{
    setPaymentRows();
  }
}
function updateSoldAmount(){
  /*
   * update the sold amount
   */
  var topay = getToPayAfterDeposit();
  var sold = topay - computePaymentRows();
  console.log("The sold is now : %s", sold);
  setSoldAmount(sold);
}
function getAmountInput(textval, id){
  /*
   * Return an amount input
   */
  var args = {id:id, amount:textval};
  var tmpl = $('#paymentAmountTmpl').template();
  return $.tmpl( tmpl, args );
}
function setPaymentRowsToEditable(){
  /*
   * Update payment rows to change the amount to a html input
   * On load, we don't know if the payment lines we get are editable
   * by default we assume they are readonly, so we change them
   * at startup if needed
   */
  if ($('#paymentcontainer').is('.paymentline')){
    $('#paymentcontainer .paymentline .paymentamount').each(function(){
      var textval = $(this).find('.input').text();
      // Parent node is the paymentline, we get the id there
      var myid = getIdFromTagId( 'paymentline_', $(this).parent().attr('id') );
      $(this).empty().html(getAmountInput(textval, myid));
    });
  }else{
    setPaymentRows();
  }
}
function initialize(){
  /*
   *  Initialize the estimation UI
   */
  if (getNbPayments() < 1 ){
     /*
      * Add a row if needed and update rows to fit manual configuration
      * (set them editable for example)
      */
     console.log("Manual payments");
     setPaymentRowsToEditable();
  }
  $(Facade).bind('linechange', function(event, element){
    computeEstimationRow(element);
  });
  $(Facade).bind('totalchange', function(event){
    computeTotal();
  });
  $(Facade).bind('linedelete', function(event, element){
    computeTotal();
  });
  $(Facade).bind('depositchange', function(event){
    setDeposit();
    updatePaymentRows();
  });
  $(Facade).bind('payment_timeschange', function(event){
    setPaymentRows();
  });
  $(Facade).bind('paymentlinechange', function(event){
    updateSoldAmount();
  });
  $(Facade).bind('totalchange', function(event){
    setDeposit();
    updatePaymentRows();
  });

  $('.estimationline').each(function(){
    $(Facade).trigger('linechange', this);
  });
  $(Facade).trigger('totalchange');
  $('select[name=tva]').change(function(){
    $(Facade).trigger('totalchange');
  });
  $('#deform textarea').first().focus();
}

