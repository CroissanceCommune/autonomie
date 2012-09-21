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
/*
 * Facade is the facade object used to dispatch events beetween elements
 * since the model is quite simple we don't build a real mvc and keep it flat
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
function formatPrice(price, rounded) {
  /*
   * Return a formatted price for display
   * @price : compute-formatted price
   */
  var dots, splitted, cents, ret_string;
  if (rounded){
    price = Math.floor(price*100) / 100;
  }

  splitted = String(price).split('.');
  if (splitted[1] != undefined){
    cents = splitted[1];
    if (cents.length>4){
      dots = true;
    }
    cents = cents.substr(0, 4);
    cents = trailingZeros(cents, rounded);
  }else{
    cents = '00';
  }
  ret_string = splitted[0] + "," + cents;
  if (dots){
    ret_string += "...";
  }
  return ret_string;
}
function isNotFormattable(amount){
  var test = " " + amount;
  if ((test.indexOf("€") >= 0 )||(test.indexOf("&nbsp;&euro;")>=0)){
    return true;
  }
  return false;
}
function formatAmount( amount, rounded ){
  /*
   * return a formatted user-friendly amount
   */
  if ( rounded === undefined ){
    rounded = true;
  }
  if (isNotFormattable(amount)){
    return amount;
  }
  return formatPrice( amount, rounded ) + "&nbsp;&euro;";
}
function trailingZeros(cents, rounded) {
  /*
   * Handle the trailing zeros needed for an amount
   */
   if (cents.length === 1){
    cents += 0;
   }
   if ( ! rounded ){
    if ( cents.length > 2 ){
      if (cents.charAt(3) == "0"){
        cents = cents.substr(0,3);
      }
      if (cents.charAt(2) == "0"){
        cents = cents.substr(0,2);
      }
    }
   }
   return cents;
}

/*
 *
 * Dom manipulation
 *
 */
function delRow(id){
  /*
   * Remove the estimation line of id 'id'
   */
  $('#' + id).remove();
  $(Facade).trigger("linedelete");
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
   * @selector : jquery selector
   * @parseStr : base string
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
function parseDate(isoDate){
  /*
   * Returns a js Date object
   */
   var splitted = isoDate.split('-');
   var year = parseInt(splitted[0], 10);
   var month = parseInt(splitted[1], 10) - 1;
   var day = parseInt(splitted[2], 10);
   return new Date(year, month, day);
}
function formatPaymentDate(isoDate){
  /*
   *  format a date from iso to display format
   */
  if (isoDate !== ''){
    return $.datepicker.formatDate("dd/mm/yy", parseDate(isoDate));
  }else{
    return "";
  }
}

/*
 *
 * Computation function
 *
 */

function getTvaPart(total, tva){
  return total * tva / 10000;
}

var Row = Backbone.Model.extend({
  /*
   * Main row model
   */
  initialize:function(tag){
    this.id = Math.random();
    this.row = $(tag);
    this.tva = this.TVA();
    this.ht = this.HT();
    this.tva_amount = this.TVAPart();
    this.ttc = this.TTC();
  },
  HT:function(){
    return 0;
  },
  TVA:function(){
    var tva = this.row.find("select[name=tva]").val();
    if (tva <0){
      tva = 0;
    }
    return tva;
  },
  TVAPart:function(){
    return getTvaPart(this.ht, this.tva);
  },
  TTC:function(){
    return this.ht + this.tva_amount;
  },
  update:function(){
    var totalinput = this.row.find(".linetotal .input");
    totalinput.empty().html( formatAmount(this.HT(), false) );
    return this.row;
  }
});

var TaskRow = Row.extend({
  /*
   *  Task Row model
   */
  type:"task",
  getCost: function(){
    return this.row.find("input[name=cost]").val();
  },
  getQuantity:function(){
    return this.row.find("input[name=quantity]").val();
  },
  HT:function(){
    var q = this.getQuantity();
    var c = this.getCost();
    return transformToCents(c) * transformToCents(q);
  }
});
var DiscountRow = Row.extend({
  /*
   *  Discount Row model
   */
  type:"discount",
  getAmount:function(){
    var amount = this.row.find("input[name=amount]").val();
    return transformToCents(amount);
  },
  HT:function(){
  console.log(this.getAmount());
    return -1 * this.getAmount();
  }
});

var RowCollection = Backbone.Collection.extend({
  /*
   *  Row collection model
   */
  elems:[],
  load:function(selector, factory){
    // this in the each function will be the iterator's item
    var _this=this;
    $(selector).each(function(){
      var row = new factory(this);
      _this.add(row);
    });
  },
  HT:function(type){
    var sum = 0;
    this.each(function(item){
      if (type != undefined){
        if (item.type == type){
          sum += item.ht;
        }
      }else{
        sum += item.ht;
      }
    });
    return sum;
  },
  TTC:function(type){
    var sum = 0;
    this.each(function(item){
      sum += item.ttc;
    });
    return sum;
  },
  Tvas:function(){
    var tvas = {};
    this.each(function(item){
      var tva_amount = item.tva_amount;
      var tva = item.tva;
      if (tva in tvas){
        tva_amount += tvas[tva];
      }
      tvas[tva] = tva_amount;
    });
    return tvas;
  }
});

var Payment = Backbone.Model.extend({

});

function getTvaLine(tva, tva_amount){
  /*
   * Return the tva display line
   */
  var label = tva /100 + " %";
  var template = $( '#tvaTmpl' ).template();
  return $.tmpl(template, {'label':label, 'value':formatAmount(tva_amount)});
}
function getExpenses(){
  /*
   *  Return the current expense configured
   */
  return transformToCents( $('input[name=expenses]').val() );
}
function getCollection(){
  /*
   * Return the collection of rows related to the payment information
   */
  var collection = new RowCollection();
  collection.load('.taskline', TaskRow);
  collection.load('.discountline', DiscountRow);
  return collection;
}
function computeTotal(){
  /*
   * Compute the main totals
   */
  console.log("Computing total");
  var collection = getCollection();
  var tasklines_ht = collection.HT("task");
  var total_ht = collection.HT();
  var total_ttc = collection.TTC();
  var tvas = collection.Tvas();
  console.log(total_ttc);
  console.log(total_ht);
  console.log(tvas);
  $('#tasklines_ht .input').empty().html(formatAmount(tasklines_ht, false));
  $('#tvalist').empty();
  for (var index in tvas){
    var line = getTvaLine(index, tvas[index]);
    $('#tvalist').append(line);
  }
  $('#total_ht .input').empty().html(formatAmount(total_ht));
  $('#total_ttc .input').empty().html(formatAmount(total_ttc));
  var expenses = getExpenses();
  var total = total_ttc + expenses;
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
  var sum = 0;
  $(".paymentline input:text[name=amount]").each(function(){
    sum += transformToCents($(this).val());
  });
  return sum;
}
function setPaymentRows(){
  /*
   * Compute and set the payment amounts
   */
  $("#paymentcontainer").empty();
  var nbpayments = getNbPayments();
  var topay = getToPayAfterDeposit();
  if (nbpayments === -1){
    // we ask for manual payment configuration
    // we want two lines (one manually configured,
    //  one fitting the total value)
    setDividedPayments(topay, 2, false);
  }else{
    setDividedPayments(topay, nbpayments);
  }
}
function computeDividedAmount(total, nbpayments){
  /*
   * Compute the divided amounts for payments rows
   */
  if (nbpayments > 1){
    var p = total * 100 / nbpayments;
    return Math.round( p / 100 );
  }else{
    return 0;
  }
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
    part = computeDividedAmount(total, nbpayments);
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
  var date = new Date();
  if ((args['paymentDate'] !== undefined) && (args['paymentDate'] !== "")) {
    date = parseDate(args['paymentDate']);
  }
  // We update the date information to fit the configured
  // display format
  $("#paymentDate_" + args['id']).datepicker({
                altField:"#paymentDate_" + args['id'] + "_altField",
                altFormat:"yy-mm-dd",
                dateFormat:"dd/mm/yy"
                });
  $("#paymentDate_" + args['id']).datepicker('setDate', date);
}
function getNbPayments(){
  /*
   * Return the number of configured payments
   */
  return parseInt($("select[name=payment_times]").val(), 10);
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
function computeDeposit(total, percent){
  /*
   *  Compute the expected account
   */
  return total * percent / 100;
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
  var total = getTotal();
  var percent = getDepositPercent();
  return computeDeposit(total, percent);
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
  $('#paymentline_1000 .paymentamount .input').html(formatAmount(value));
  $('#paymentline_1000 .paymentamount input[name=amount]').val(value);
}
function updatePaymentRows(){
  /*
   * Update payment rows
   */
  var nbpayments = getNbPayments();
  if (nbpayments === -1){
    updateSoldAmount();
  }else{
    if ($('.paymentline').length != nbpayments){
      // Lors du refraichissement de page on peut avoir des incohérences
      setPaymentRows();
    }else{
      updateDividedPaymentAmounts(nbpayments);
    }
  }
}
function updateDividedPaymentAmounts(nbpayments){
  /*
   *  Update divided payments amounts
   */
  var topay = getToPayAfterDeposit();
  if (nbpayments == 1){
    setSoldAmount(topay);
  }else{
    var part = computeDividedAmount(topay, nbpayments);
    setDividedPaymentRowsAmount(part);
    var rest = topay - ( part * (nbpayments - 1));
    setSoldAmount(rest);
  }
}
function setDividedPaymentRowsAmount(amount){
  /*
   *  update payment rows' amount
   */
  $('#paymentcontainer .paymentline').each(function(){
      $(this).find('.input').html(formatAmount(amount));
      $(this).find('input[name=amount]').val(amount);
   });
}
function updateSoldAmount(){
  /*
   * update the sold amount
   */
  var topay = getToPayAfterDeposit();
  var sold = topay - computePaymentRows();
  setSoldAmount(sold);
}
function getAmountInput(args){
  /*
   * Return an amount input
   */

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
  if (!(jQuery.isEmptyObject($('#paymentcontainer .paymentline')))){
    $('#paymentcontainer .paymentline .paymentamount').each(function(){
      var args = {};
      args['amount'] = $(this).find('.input').text();
      // Parent node is the paymentline, we get the id there
      args['id'] = getIdFromTagId( 'paymentline_', $(this).parent().attr('id') );

      if (!(jQuery.isEmptyObject($(this).find('.error')))){
        args['amount_error'] = $(this).find('.error').text();
      }
      $(this).replaceWith(getAmountInput(args));
    });
  }else{
    setPaymentRows();
  }
}
function initialize(){
  /*
   *  Initialize the estimation UI
   */
  var row;
  if (getNbPayments() < 1 ){
     /*
      * Add a row if needed and update rows to fit manual configuration
      * (set them editable for example)
      */
     setPaymentRowsToEditable();
  }
  $(Facade).bind('linechange', function(event, element){
  console.log("Line changed");
    if ($(element).find("input[name=amount]").length === 0){
      row = new TaskRow(element);
      row.update();
    }else{
      row = new DiscountRow(element);
      row.update();
    }
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

  $('.taskline').each(function(){
    $(Facade).trigger('linechange', this);
  });
  $('.discountline').each(function(){
    $(Facade).trigger('linechange', this);
  });
  $(Facade).trigger('totalchange');
  $('select[name=tva]').change(function(){
    $(Facade).trigger('totalchange');
  });
  $('#deform textarea').first().focus();
}

