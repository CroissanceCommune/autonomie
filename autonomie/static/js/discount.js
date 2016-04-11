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
    this.el.find(".form-group").removeClass('has-error');
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
    this.container = container;
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
    var textarea = line.children().find("textarea");
    textarea.val(description);
    tinyMCE.get(textarea.attr('id')).setContent(description);
    line.children().find("input[name=amount]").val(value);
    line.children().find("select[name=tva]").val(tva);
    setDiscountLinesBehaviours();

    $(Facade).trigger("linechange", line);
    $(Facade).trigger('totalchange', line);
  }
};

var catalog = {
  ui: {
    el: "#catalog_popup",
    search_input: "#catalog_popup input",
    tree: "#catalog_popup .tree-container",
    valid_btn: "#catalog_popup button.btn-success",
    cancel_btn: "#catalog_popup button.btn-danger"
  },
  popup: function(type, add_button){
    this.currentType = type;
    this.add_button = add_button;
    this.show(type);
    return false;
  },
  show: function(type){
    /*
     * Build the js tree of our catalog for the given type
     */
    this.ui.tree.jstree('destroy');
    var url = AppOptions['load_catalog_url'];
    var load_catalog = ajax_request(url, {type: this.currentType});
    load_catalog.then(this.buildJsTree);
  },
  buildJsTree: function(result){
    /*
     * Build the jstree object
     */
    if (_.has(result, "void_message")){
      this.ui.tree.html(result.void_message);
      this.ui.valid_btn.prop('disabled', true);
      this.ui.search_input.prop('disabled', true);
      this.setCancelOnClick();
      this.ui.el.dialog('open');
    } else {
      this.ui.search_input.prop('disabled', false);
      this.ui.valid_btn.prop('disabled', false);
      this.ui.tree.jstree({
        plugins: ["checkbox", 'types', "search"],
        types: {
          "default": {icon: "glyphicon glyphicon-triangle-right"},
          product: {icon: "glyphicon glyphicon-file"},
          group: {icon: "glyphicon glyphicon-book"}
        },
        search: {
          case_insensitive: true,
          show_only_matches: true
        },
        core: { data: result.jstree}
      });
      this.ui.tree.on('ready.jstree', this.afterJstreeLoaded);
    }
  },
  afterJstreeLoaded: function(e, data){
    console.log("AfterJstreeLoaded");
      this.setCancelOnClick();
      this.ui.el.dialog('open');
      this.setValidOnclick();
      this.setSearchBheaviour();
  },
  setSearchBheaviour: function(){
    var this_ = this;
    this.ui.search_input.off("keyup");
    this.ui.search_input.on("keyup", function() {
      var searchString = $(this).val();
      this_.ui.tree.jstree('search', searchString);
    });
  },
  getLastSeqItem: function(add_button){
    /* Returns the last sequence item added to the sequence managed by
     * the add button
     *
     * :param add_button: The Add button
     */
    var seq = $(add_button).closest('.deformSeq');
    var seq_container = seq.children('.deformSeqContainer').first();
    var item = seq_container.children('.deformSeqItem').last();
    return item;
  },
  scrollToElement: function(element){
    $('html, body').animate({
      scrollTop: element.offset().top
    }, 500);
  },
  getLineAddButton: function(group){
    /*
     * Returns the add line button nested in the given group
     */
    return group.find('button.taskline-add').first();
  },
  addProductLine: function(node_datas, add_button){
    /*
     * Add a product line to the add_button provided as argument
     *
     * :param node_datas: The datas describing the configured product
     * :param add_button: The add line button (default this.add_button)
     */
    add_button = add_button || this.add_button;
    deform.appendSequenceItem(add_button);
    var line = this.getLastSeqItem(add_button);
    var textarea = line.children().find("textarea");
    textarea.val(node_datas.description);
    tinyMCE.get(textarea.attr('id')).setContent(node_datas.description);
    line.children().find("input[name=cost]").val(node_datas.value);
    line.children().find("input[name=quantity]").val(1);
    line.children().find("select[name=tva]").val(node_datas.tva);
    line.children().find("select[name=unity]").val(node_datas.unity);
    setTaskLinesBehaviours();
    fireAmountChange(line.children().find("input[name=cost]"));
    highlight(line);
    return line;
  },
  addProductGroup: function(node_datas){
    deform.appendSequenceItem(this.add_button);
    var group = this.getLastSeqItem(this.add_button);
    group.children().find("input[name=title]").first().val(node_datas.title);
    group.children().find("textarea").first().val(node_datas.description);

    var add_line_button = this.getLineAddButton(group);
    var this_ = this;
    _.each(node_datas.products, function(product){
      this_.addProductLine(product, add_line_button);
    });
    this.scrollToElement(group);
    return group;
  },
  addNode: function(node_datas){
    if (this.currentType == 'sale_product'){
      this.addProductLine(node_datas);
    }else{
      this.addProductGroup(node_datas);
    }
  },
  insertSelectedElements: function(){
    var this_ = this;
    var ajax_reqs = [];
    _.each(this.ui.tree.jstree('get_selected', true), function(node){
      if (_.has(node.original, 'url')){
        var ajax_load = ajax_request(node.original.url, {}, {type: 'GET'});
        ajax_load.then(this_.addNode);
        ajax_reqs.push(ajax_load);
      }
    });
    // To pass an array of values to any function that normally expects them to
    // be separate parameters, use Function.apply
    $.when.apply($, ajax_reqs).then(this.close);
  },
  close:function(){
    this.ui.el.dialog('close');
  },
  setValidOnclick: function(){
    /*
     * Set the onclick behaviour for the success button
     */
    this.ui.valid_btn.attr('disabled', false);
    this.ui.valid_btn.off('click.catalog');
    this.ui.valid_btn.on('click.catalog', this.insertSelectedElements);
  },
  setCancelOnClick: function(){
    /*
     * Set the onclick behaviour for the cancel button
     */
    this.ui.cancel_btn.off('click.catalog');
    this.ui.cancel_btn.on('click.catalog', this.close);
  },
  init: function(){
    loadUI(this.ui);
    setPopUp(this.ui.el, "Catalogue produit");

    // Ensure this is the catalog object
    _.bindAll(this, "buildJsTree", "insertSelectedElements", "close",
    "addNode", "addProductLine", "setSearchBheaviour", "afterJstreeLoaded");
  }
};
$(function(){
  catalog.init();
});
