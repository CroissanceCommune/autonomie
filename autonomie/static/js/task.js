/*
 * * Copyright (C) 2012-2013 Croissance Commune
 * * Authors:
 *       * Arezki Feth <f.a@majerti.fr>;
 *       * Miotte Julien <j.m@majerti.fr>;
 *       * Pettier Gabriel;
 *       * TJEBBES Gaston <g.t@majerti.fr>
 *
 * This file is part of Autonomie : Progiciel de gestion de CAE.
 *
 *    Autonomie is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    Autonomie is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
 */


window.AppOptions = window.AppOptions || {};
var Facade = new Object();
var Selectors = {
  expenses_ht: 'input[name=expenses_ht]',
  expenses: 'input[name=expenses]',
  totalinput: ".linetotal .input",
  tva: "select[name=tva]",
  cost: "input[name=cost]",
  quantity: "input[name=quantity]",
  amount: "input[name=amount]",
  default_tva: 'input[name=default_tva]',
  taskline: ".taskline",
  group_taskline: ".linegroup .taskline",
  discountline: ".discountline",
  discount_headers: "#discount-header",
  tasklines_ht: "#tasklines_ht .input",
  linegroup_ht: ".linegroupamount",
  tvalist: "#tvalist",
  total_ht: "#total_ht .input",
  total_ttc: "#total_ttc .input",
  total: '#total .input',
  deform_close: ".deformClosebutton"
};

function delRow(id){
  /*
   * Remove the estimation line of id 'id'
   */
  $('#' + id).remove();
  $(Facade).trigger("linedelete");
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
    if (this.row.parents('.linegroup').length > 0){
      this.linegroup = this.row.parents('.linegroup');
    } else {
      this.linegroup = null;
    }
  },
  HT:function(){
    return 0;
  },
  TVA:function(){
    var tva = this.row.find(Selectors.tva).val();
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
    var totalinput = this.row.find(Selectors.totalinput);
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
    return this.row.find(Selectors.cost).val();
  },
  getQuantity:function(){
    return this.row.find(Selectors.quantity).val();
  },
  HT:function(){
    var q = this.getQuantity();
    var c = this.getCost();
    return strToFloat(c) * strToFloat(q);
  }
});
var DiscountRow = Row.extend({
  /*
   *  Discount Row model
   */
  type:"discount",
  getAmount:function(){
    var amount = this.row.find(Selectors.amount).val();
    return strToFloat(amount);
  },
  HT:function(){
  console.log(this.getAmount());
    return -1 * this.getAmount();
  }
});
var ExpenseRow = Row.extend({
  /*
   * HT Expense row
   */
  type:'expense',
  TVA:function(){
    // This tva value should be set dynamically
    var tva_object = _.find(
      AppOptions['tvas'], function(val){return val['default'];}
    );
    if (_.isUndefined(tva_object)){
      return strToFloat("0");
    }else{
      var tva = tva_object.value.toString();
      return strToFloat(tva);
    }
  },
  HT:function(){
    return strToFloat(this.row.val());
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
  Tvas:function(type){
    var tvas = {};
    var tva_amount;
    var tva;
    this.each(function(item){
      if (type !== undefined){
        if (item.type == type){
          tva_amount = item.tva_amount;
          tva = item.tva;
          if (tva in tvas){
            tva_amount += tvas[tva];
          }
          tvas[tva] = tva_amount;
        }
      } else {
        tva_amount = item.tva_amount;
        tva = item.tva;
        if (tva in tvas){
          tva_amount += tvas[tva];
        }
        tvas[tva] = tva_amount;
      }
    });
    return tvas;
  },
  HT_per_Tvas:function(type){
    var hts = {};
    var tva;
    var ht;
    this.each(function(item){
      if (type !== undefined){
        if (item.type == type){
          ht = item.ht;
          tva = item.tva;
          if (tva in hts){
            ht += hts[tva];
          }
          hts[tva] = ht;
        }
      } else {
        ht = item.ht;
        tva = item.tva;
        if (tva in hts){
          ht += hts[tva];
        }
        hts[tva] = ht;
      }
    });
    return hts;
  },
  HT_per_group: function(group_obj){
    var ht = 0;
    this.each(function(item){
      if (item.linegroup !== null){
        if (item.linegroup.is(group_obj)){
          ht += item.ht;
        }
      }
    });
    return ht;
  }
});

var Payment = Backbone.Model.extend({

});

function getTvaLine(tva, tva_amount){
  /*
   * Return the tva display line
   */
  var label = tva /100 + " %";
  var datas = {'label':label, 'value':formatAmount(tva_amount)};
  return Handlebars.templates['tvalist.mustache'](datas);
}
function getExpensesHT() {
  /*
   * Return the current HT expenses configured
   */
  return strToFloat( $(Selectors.expenses_ht).val() );
}
function getCollection(){
  /*
   * Return the collection of rows related to the payment information
   */
  var collection = new RowCollection();
  collection.load(Selectors.taskline, TaskRow);
  collection.load(Selectors.discountline, DiscountRow);
  collection.add(new ExpenseRow(Selectors.expenses_ht));
  return collection;
}
function computeTotal(){
  /*
   * Compute the main totals
   */
  var collection = getCollection();
  var tasklines_ht = collection.HT("task");
  var total_ht = collection.HT();

  var linegroups = $('.linegroup');

  _.each(linegroups, function(item){
    var linegroup = $(item);
    var linetotal = collection.HT_per_group(linegroup);
    var display_total = formatAmount(linetotal, false);
    linegroup.find('.grouplinetotal .input').empty().html(display_total);
  });

  var total_ttc = collection.TTC();
  var tvas = collection.Tvas();
  console.log(total_ttc);
  console.log(total_ht);
  console.log(tvas);
  $(Selectors.tasklines_ht).empty().html(formatAmount(tasklines_ht, false));
  $(Selectors.tvalist).empty();
  for (var index in tvas){
    var line = getTvaLine(index, tvas[index]);
    $(Selectors.tvalist).append(line);
  }
  $(Selectors.total_ht).empty().html(formatAmount(total_ht));
  $(Selectors.total_ttc).empty().html(formatAmount(total_ttc));
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
    sum += strToFloat($(this).val());
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
  if (manualDeliverables(nbpayments)){
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
    var p = Math.round(total * 100 / nbpayments);
    return  p / 100;
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
    if (manualDeliverables()){
      args['readonly'] = false;
    }else{
      args['readonly'] = true;
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
function manualDeliverables(nbpayments){
  if (_.isUndefined(nbpayments)){
    nbpayments = getNbPayments();
  }
  return nbpayments == -1;
}
function getPaymentRow(args){
  /*
   *  return a payment line in html format
   *  @param:args: templating datas
   */
  var template = Handlebars.templates['payment.mustache'];
  html = template( args );
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
    $("#account_container").show();
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
  var total = getTotal();
  var percent = getDepositPercent();
  return getPercent(total, percent);
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
    return strToFloat(deposit);
}
function getTotal(){
  /*
   * Return the current total
   */
  return strToFloat($(Selectors.total_ttc).text());
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
  if (manualDeliverables(nbpayments)){
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

  var tmpl = Handlebars.templates['paymentAmount.mustache'];
  return tmpl( args );
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
    $('#paymentcontainer .paymentline').each(function(){
      $(this).find('input[name=amount]').blur(function(){
        $(Facade).trigger('paymentlinechange');
      });
    });
  }else{
    setPaymentRows();
  }
}
function fetchFormOptions(){
  /*
   * Get form options from the server
   */
  if (AppOptions['loadurl'] !== undefined){
    $.ajax({
      url: AppOptions['loadurl'],
      dataType: 'json',
      async: false,
      mimeType: "textPlain",
      data: {},
      success: function(data) {
        _.extend(AppOptions, data);
      },
      error: function(){
        alert("Une erreur a été rencontrée, contactez votre administrateur.");
      }
    });

  }else{
    alert("Une erreur a été rencontrée, contactez votre administrateur.");
  }
}
function fetchFormContext(){
  /*
   * In case of edition, get the context in json format and build some form
   * fields regarding the datas
   */
  var url = document.URL;
  $.ajax({
    url: url,
    dataType: 'json',
    cache:false,
    success: function(datas){
      console.log(datas);
    }
  });
}
function fireAmountChange(event){
  /*
   * Fire an amount change on the line containing the current form_element
   *
   * :param obj event: The jquery event object or the input which changed
   */
  var input_tag;
  if (event.target){
    input_tag = $(event.target);
  }else {
    console.log("Not an event");
    return;
  }
  var row = input_tag.parent().parent().parent();
  $(Facade).trigger("linechange", row);
  $(Facade).trigger("totalchange", row);
  return;
}
function fireTvaChange(){
  onTvaSelect(this);
  fireAmountChange();
}
function addTaskLine(link_dom_element){
  deform.appendSequenceItem(link_dom_element);
  setTaskLinesBehaviours();
  return false;
}
function setTaskLinesBehaviours(){
  /*
   * Set the field behaviours on page load
   */
  var s = Selectors.taskline + " " + Selectors.cost;
  s = $(s);
  s.off("blur");
  s.on("blur", fireAmountChange);

  s = Selectors.taskline + " " + Selectors.quantity;
  s = $(s);
  s.off("blur");
  s.on("blur", fireAmountChange);

  s = Selectors.taskline + " " + Selectors.tva;
  s = $(s);
  s.off('change');
  s.on('change', fireTvaChange);

  s = $(Selectors.taskline + " " + Selectors.deform_close);
  s = $(s);
  s.removeAttr('onclick');
  s.off('click.removeit');
  s.on("click.removeit", function(){
    deform.removeSequenceItem(this);
    computeTotal();
  });
}
function setDiscountLinesBehaviours(){
  /*
   * Set the field behaviours on page load
   */
  var s = Selectors.discountline + " " + Selectors.amount;
  $(s).off("blur");
  $(s).on("blur", fireAmountChange);

  s = Selectors.discountline + " " + Selectors.tva;
  $(s).off('change');
  $(s).on('change', fireAmountChange);

  s = $(Selectors.discountline + " " + Selectors.deform_close);
  s = $(s);
  s.removeAttr('onclick');
  s.off('click.removeit');
  s.on("click.removeit", function(){
    deform.removeSequenceItem(this);
    computeTotal();
  });
}
function toggleDiscountHeader(){
  /*
   * Show or hide the discount header
   */
  if ($(Selectors.discountline).length > 0){
    $(Selectors.discount_headers).removeClass('hidden');
  } else {
    $(Selectors.discount_headers).addClass('hidden');
  }
}
function setExpenseBehaviour(){
  /*
   * set the behaviour on expense ht change
   */
  $(Selectors.expenses_ht).off('blur');
  $(Selectors.expenses_ht).on('blur', fireAmountChange);
}
function setPaymentsBehaviour(){
   $('select[name=deposit]').change(function(){
      $(Facade).trigger('depositchange', this);
  });
  $('select[name=payment_times]').change(function(){
      $(Facade).trigger('payment_timeschange', this);
  });
}
/*
 * Set behaviours for payment conditions change
 */
var payment_condition_handler = {
  getEl: function() {
    return $("select[name=payment_conditions_select]");
  },
  set: function(val) {
    $("textarea[name=payment_conditions]").val(val);
  },
  selected: function() {
    return this.getEl().children('option:selected').html();
  },
  change: function(){
    option = this.selected();
    if (option !== ''){
      this.set(option);
    }
  }
};

function initialize(){
  /*
   *  Initialize the document edition UI
   */
  fetchFormOptions();
  if (AppOptions['edit']){
    fetchFormContext();
  }
  setTaskLinesBehaviours();
  setDiscountLinesBehaviours();
  setExpenseBehaviour();
  if (typeof(initPaymentRows) !== 'undefined'){
    initPaymentRows();
  }
  if ( manualDeliverables() ){
     /*
      * Add a row if needed and update rows to fit manual configuration
      * (set them editable for example)
      */
     setPaymentRowsToEditable();
  }
  setPaymentsBehaviour();
  var row;
  $(Facade).bind('linechange', function(event, element){
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

  /*
   * We trigger the changes on page load
   */
  $('.row').each(function(){
    $(Facade).trigger('linechange', this);
  });
  $(Facade).trigger('totalchange');
  $('select[name=tva]').change(function(){
    onTvaSelect(this);
    $(Facade).trigger('totalchange');
  });
  cleanProductSelects();
  $('#deform textarea').first().focus();

  payment_condition_handler.getEl().change(
    function(){
      payment_condition_handler.change();
    }
  );
  $('#deform').on('submit', function(){
    showLoader();
    $(this).on('submit', function(){
      alert('Vous ne pouvez valider deux fois le même formulaire. Actualisez la page.');
      return false;
    });
    return true;
  });
}
$(function(){
  initialize();
});
