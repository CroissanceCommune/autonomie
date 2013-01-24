/*
 * File Name : discount.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 * Tools to handle discount configuration
 */
var Discount = Backbone.Model.extend({
  /* Common model for discounts */
});

var PercentDiscount = Discount.extend({
  /*
   * Percent based discount
   * Is a percent of some lines of all of them
   */
  defaults:{
    percent:0,
    selectors:[]
  },
  totalHT:function(){
    $(selectors).each(function(selector){

    });
  },
  HTs:function(){
  /*
   * Return the discount HT value
   */
    percent(totalHT(), this.percent);
  }
});

var StaticDiscount = Discount.extend({
  /*
   * Static discount with cost and tva
   */
  defaults:{
    cost:0,
    quantity:1
  },
  HT:function(){
    return transformToCents(-1 * this.cost);
  }
});

var DiscountView = Backbone.Marionette.ItemView.extend({
  template:"#discount_item"
});

var DiscountList =  Backbone.Marionette.CollectionView.extend({
  itemView: DiscountView
});

var discount = {
  el:null,
  select:null,
  percent_tag:null,
  value_tag:null,
  container:null,
  get_select:function(){
    return this.el.find("select");
  },
  get_selected:function(){
    return this.select.children('option:selected').val();
  },
  get_description:function(){
    return this.el.find("textarea[name=discount_temp_description]").val();
  },
  get_percent:function(){
    return this.el.find("input[name=discount_temp_percent]").val();
  },
  get_percent_tag:function(){
    return $("#percent_configuration");
  },
  get_value:function(){
    return this.el.find("input[name=discount_temp_value]").val();
  },
  get_value_tag:function(){
    return $("#value_configuration");
  },
  get_tva:function(){
    return "700";
  },
  void_all:function(){
    this.percent_input.val('');
    this.value_input.val('');
  },
  set_switch:function(){
    var this_ = this;
    this.select.change(function(){
      if (this_.get_selected() == 'percent'){
        this_.percent_tag.show();
        this_.value_tag.hide();
      }else{
        this_.percent_tag.hide();
        this_.value_tag.show();
      }
    });
  },
  popup:function(container){
    this.container = $(container).parent().parent();
    this.el = $('#discount_popup');
    this.value_tag = this.get_value_tag();
    this.percent_tag = this.get_percent_tag();
    this.select = this.get_select();
    this.el.dialog('open');
    this.set_switch();
  },
  close:function(){
    this.el.dialog('close');
  },
  create_percent_based_discounts:function(){
    var collection = getCollection();
    var hts = collection.HT_per_Tvas();
    var percent = this.get_percent();
    var description = this.get_description();
    for (var tva in hts){
      var ht_amount = hts[tva];
      var value = getPercent(ht_amount, percent);
      this.add_line(description, value, tva);
    }
  },
  create_value_based_discounts:function(){
    var description = this.get_description();
    var value = this.get_value();
    var tva = this.get_tva();
    this.add_line(description, value, tva);
  },
  validate:function(){
    if (this.get_selected() == 'percent'){
      this.create_percent_based_discounts();
    }else{
      this.create_value_based_discounts();
    }
    this.el.dialog('close');
  },
  add_line:function(description, value, tva){
    deform.appendSequenceItem(this.container);
    var line = $('.discountline').last();
    line.children().find("textarea").val(description);
    line.children().find("input[name=amount]").val(value);
    line.children().find("select[name=tva]").val(tva);
  }
};
