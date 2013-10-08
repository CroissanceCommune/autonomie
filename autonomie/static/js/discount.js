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


var validators = {
  /* """
   * Form Validation tool
   */
  number: /^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/,
  isNumber:function(value){
    return _.isNumber(value) || (_.isString(value) && value.match(this.number));
  },
  hasValue:function(value) {
      return !(_.isNull(value) || _.isUndefined(value) ||
                    (_.isString(value) && trim(value) === ''));
  },
  isInRange:function(value, min, max){
    return this.isNumber(value) && value >= min && value <= max;
  }
};
var discount = {
  /*"""
   * Discount handling object
   * Handle the popup used to configure discounts and add lines regarding
   * the configured values
   */
  el:null,
  select:null,
  percent_tag:null,
  value_tag:null,
  container:null,

  get_select:function(){
    /*"""
     * Return the select used to choose the discount type
     */
    return this.el.find("select");
  },
  get_selected:function(){
    /*"""
     * Return the current selected value
     */
    return this.select.children('option:selected').val();
  },
  get_description:function(){
    /*"""
     *Return the current configured description
     */
    return this.get_description_textarea().val();
  },
  get_description_textarea:function(){
    /*"""
     *  Return the configured description
     */
    return this.el.find("textarea[name=discount_temp_description]");
  },
  get_percent:function(){
    /*"""
     * Return the percents that have been configured
     */
    return this.get_percent_input().val();
  },
  get_percent_input:function(){
    /*"""
     * Return the input used to configure the percents
     */
    return this.el.find("input[name=discount_temp_percent]");
  },
  get_percent_tag:function(){
    /*"""
     * Return the container for percent configuration
     */
    return $("#percent_configuration");
  },
  get_value:function(){
    /*"""
     *  Return the value for simple discount configuration
     */
    return this.get_value_input().val();
  },
  get_value_input:function(){
    /*"""
     *  Return the input used to configure the value of our dicount
     */
    return this.el.find("input[name=discount_temp_value]");
  },
  get_value_tag:function(){
    /*"""
     *  Return the container for discount by-value configuration
     */
    return $("#value_configuration");
  },
  get_tva_select:function(){
    /*"""
     * Return the tva select object
     */
    return this.el.find("select[name=discount_temp_tva]");
  },
  get_tva:function(){
    /*"""
     *  Return the current configured tva
     */
    return this.get_tva_select().val();
  },
  void_all:function(){
    this.get_percent_input().val('');
    this.get_value_input().val('');
    this.get_description_textarea().val();
    this.el.find(".control-group").removeClass('error');
    this.el.find(".help-inline.error-message").remove();
    this.select.change();
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
    this.set_switch();
    this.void_all();
    this.el.dialog('open');
  },
  close:function(){
    this.el.dialog('close');
  },
  create_percent_based_discounts:function(){
    var collection = getCollection();
    // We don't want expenses to be part of the discount computation
    var hts = _.extend(collection.HT_per_Tvas('task'),
                      collection.HT_per_Tvas('discounts'));
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
      if (this.validate_percent()){
        this.create_percent_based_discounts();
       this.el.dialog('close');
      }
    }else{
      if (this.validate_value()){
        this.create_value_based_discounts();
        this.el.dialog('close');
      }
    }
  },
  validate_percent:function(){
    var percent = this.get_percent();
    var tag = this.el.find("input[name=discount_temp_percent]");
    if (validators.isNumber(percent)){
      if (validators.isInRange(percent, 1, 99)){
        return true;
      }else{
        showError(tag, "n'est pas compris entre 1 et 99");
      }
    }else{
      showError(tag, "n'est pas un nombre");
    }
    return false;
  },
  validate_value:function(){
    var value = this.get_value();
    var tag = this.el.find("input[name=discount_temp_value]");
    if (validators.isNumber(value)){
      return true;
    }else{
      showError(tag, "n'est pas un nombre");
    }
    return false;
  },
  add_line:function(description, value, tva){
    deform.appendSequenceItem(this.container);
    var line = $('.discountline').last();
    line.children().find("textarea").val(description);
    line.children().find("input[name=amount]").val(value);
    line.children().find("select[name=tva]").val(tva);
    $(Facade).trigger("linechange", line);
    $(Facade).trigger('totalchange', line);
  }
};
