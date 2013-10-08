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



var AppOptions = {};
var MyApp = new Backbone.Marionette.Application();


MyApp.on("initialize:after", function(){
  /*
   *""" Launche the history (controller and router stuff)
   */
  if ((Backbone.history)&&(! Backbone.History.started)){
    Backbone.history.start();
  }
});



/******************************** Models ********************************/
var BaseExpenseModel = Backbone.Model.extend({
  /*
   * BaseModel for expenses, provides tools to access main options
   */
  getType:function(arr){
    /*
     * Retrieve the element from arr where its type_id is the same as the model's
     * current one
     */
    var type_id = this.get('type_id');
    return _.find(arr, function(type){return type['value'] === type_id;});
  },
  getTypeOptions: function(){
    /*
     * Return an array of options for types ( should be overriden )
     */
    return [];
  },
  getTypeLabel: function(){
    /*
     * Return the Label of the current type
     */
    var options = this.getTypeOptions();
    var current_type = this.getType(options);
    if (current_type === undefined){
      return "";
    }else{
      return current_type.label;
    }
  }

});
var ExpenseLine = BaseExpenseModel.extend({
  /*
   *  Expenseline model
   *
   *  An expense line should be a tel expense or a more general one
   *
   *  It's composed of HT value, TVA value, description, expensetype id, date
   *
   *  altdate is used for display
   */
  // default values for an expenseline
  defaults:{
    category: null,
    description:"",
    ht:0,
    tva:0
  },
  // Constructor dynamically add a altdate if missing
  // (altdate is used in views for jquery datepicker)
  initialize: function(options){
    if ((options['altdate'] === undefined)&&(options['date']!==undefined)){
      this.set('altdate', formatPaymentDate(options['date']));
    }
  },
  // Validation rules for our model's attributes
  validation:{
    category: {
      required:true,
      msg:"est requise"
    },
    type_id:{
      required:true,
      msg:"est requis"
    },
    date: {
      required:true,
      pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
      msg:"est requise"
    },
    ht: {
      required:true,
      // Match"es 19,6 19.65 but not 19.654"
      pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
      msg:"doit être un nombre"
    },
    tva: {
      required:true,
      pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
      msg:"doit être un nombre"
    }
  },
  total: function(){
    var total = this.getHT() + this.getTva();
    if (this.isSpecial()){
      var percentage = this.getType(AppOptions['teltypes']).percentage;
      total = getPercent(total, percentage);
    }
    return total;
  },
  getTva:function(){
    return parseFloat(this.get('tva'));
  },
  getHT:function(){
    return parseFloat(this.get('ht'));
  },
  isSpecial:function(){
    /*
     * return True if this expense is a special one (related to phone)
     */
    return this.getType(AppOptions['teltypes']) !== undefined;
  },
  hasNoType: function(){
  var isnottel = _.isUndefined(this.getType(AppOptions['teltypes']));
  var isnotexp = _.isUndefined(this.getType(AppOptions['expensetypes']));
    if (isnottel && isnotexp){
      return true;
    }else{
      return false;
    }
  },
  getTypeOptions: function(){
    var arr;
    if (this.isSpecial()){
      arr = AppOptions['teltypes'];
    }else{
      arr = AppOptions['expensetypes'];
    }
    return arr;
  }
});


var ExpenseKmLine = BaseExpenseModel.extend({
  /*
   *  Model for expenses related to kilometers fees
   *
   *  Km fees are compound of :
   *  * kilometers
   *  * expense type id
   *  * start point
   *  * end point
   *  * description
   *
   */
  defaults:{
    category:null,
    start:"",
    end:"",
    description:""
  },
  initialize: function(options){
    if ((options['altdate'] === undefined)&&(options['date']!==undefined)){
      this.set('altdate', formatPaymentDate(options['date']));
    }
  },
  validation:{
    category: {
      required:true,
      msg:"est requise"
    },
    type_id:{
      required:true,
      msg:"est requis"
    },
    date: {
      required:true,
      pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
      msg:"est requise"
    },
    km: {
      required:true,
      // Match"es 19,6 19.65 but not 19.654"
      pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
      msg:"doit être un nombre"
    }
  },
  getIndice: function(){
    /*
     *  Return the reference used for compensation of km fees
     */
    var elem = _.where(AppOptions['kmtypes'], {value:this.get('type_id')})[0];
    if (elem === undefined){
      return 0;
    }
    return parseFloat(elem.amount);
  },
  total: function(){
    var km = this.getKm();
    var amount = this.getIndice();
    return km * amount;
  },
  getKm:function(){
    return parseFloat(this.get('km'));
  },
  getTypeOptions: function(){
    return AppOptions['kmtypes'];
  }
});


var ExpenseLineCollection = Backbone.Collection.extend({
  /*
   *  Collection of expense lines
   */
  model: ExpenseLine,
  url: "/expenses/lines",
  comparator: function( a, b ){
    /*
     * Sort the collection and place special lines at the end
     */
    var res = 0;
    if ( b.isSpecial() ){
      res = -1;
    }else if( a.isSpecial() ){
      res = 1;
    }else{
      var acat = a.get('category');
      var bcat = b.get('category');
      if ( acat < bcat ){
        res = -1;
      }else if ( acat > bcat ){
        res = 1;
      }
    }
    return res;
  },
  total: function(category){
    /*
     * Return the total value
     */
    var result = 0;
    this.each(function(model){
      if (category != undefined){
        if (model.get('category') != category){
          return;
        }
      }
      result += model.total();
    });
    return result;
  }
});


var ExpenseKmCollection = Backbone.Collection.extend({
  /*
   * Collection for expenses related to km fees
   */
  model: ExpenseKmLine,
  total: function(category){
    var result = 0;
    this.each(function(model){
      if (category != undefined){
        if (model.get('category') != category){
          return;
        }
      }
      result += model.total();
    });
    return result;
  }
});


/********************  Views  *********************************/
var BaseExpenseLineView = BaseTableLineView.extend({
  /*
   * Base item view for expense lines
   */
  _remove: function(){
    /*
     *  Delete the line
     */
    var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
    if (confirmed){
      var _model = this.model;
      this.highlight(function(){_model.destroy(
        {success: function(model, response) {
          displayServerSuccess("L'élément a bien été supprimé");
        }}
      );});
    }
  }
});

var ExpenseLineView = BaseExpenseLineView.extend({
  /*
   *  Expense Line view (for classic and tel expenses)
   */
  template: templates.expense,
  tagName:"tr",
  events: {
    'click a.remove':'_remove',
    'change input[name=ht]':'changeVal',
    'change input[name=tva]':'changeVal'
  },
  ui:{
    htinput:'input[name=ht]',
    tvainput:'input[name=tva]',
    total:'span[class=total]'
  },
  templateHelpers:function(){
    /*
     * Add custom var for rendering
     */
    var typelabel = this.model.getTypeLabel();
    var edit_url = "#lines/" + this.model.cid + "/edit";
    var total = this.model.total();
    return {typelabel:typelabel,
            edit_url:edit_url,
            total:formatAmount(total),
            edit:AppOptions['edit']};
  },
  initialize: function(){
    /*
     * View constructor
     */
    // bind the model change to the view rendering
    if (this.model.hasNoType()){
      this.template = templates.expenseorphan;
    }
    if (this.model.isSpecial()){
      this.template = templates.expensetel;
    }else{
      this.listenTo(this.model, 'change', this.render, this);
    }
  },
  changeVal: function(){
    /*
     * Called when one of the inputs have been edited
     */
    Backbone.Validation.bind(this);
    var this_ = this;
    var attrs = { ht:this.ui.htinput.val(), tva:this.ui.tvainput.val()};
    this.model.save(attrs, {
          success:function(){
            displayServerSuccess("Les informations ont bien été enregistrées");
            this_.highlight();
            this_.setTotal();
          },
          error:function(){
            displayServerError("Une erreur est survenue lors la sauvegarde" +
            " de vos données. Contactez votre administrateur.");
          },
          wait:true});
    Backbone.Validation.unbind(this);
  },
  setTotal: function(){
    var total = this.model.total();
    total = formatAmount(total);
    this.ui.total.html(total);
  }
});


var ExpenseKmLineView = BaseExpenseLineView.extend({
  /*
   *  View for expenses related to km fees
   */
  template: templates.expenseKm,
  tagName:"tr",
  events: {
    'click a.remove':'_remove'
  },
  templateHelpers:function(){
    /*
     *  Load dynamic datas for rendering
     */
    var typelabel = this.model.getTypeLabel();
    var total = this.model.total();
    var edit_url = "#kmlines/" + this.model.cid + "/edit";
    return {typelabel:typelabel,
            edit_url:edit_url,
            edit:AppOptions['edit'],
            total:formatAmount(total)};
  },
  initialize: function(){
    this.listenTo(this.model, 'change', this.render, this);
  }
});


var BaseExpenseCollectionView = Backbone.Marionette.CompositeView.extend({
  tagName: "div",
  internalContainer: "tbody.internal",
  activityContainer: "tbody.activity",
  templateHelpers:function(){
    return {edit:AppOptions['edit']};
  },
  appendHtml: function(collectionView, itemView, index){
    /*
     * Choose the container for child appending regarding the category
     */
    this.listenTo(itemView.model, 'change', this.setTotal, this);

    var childrenContainer;
    if (itemView.model.get('category') == '1'){
      // It's an expense related to internal needs
      childrenContainer = collectionView.$(collectionView.internalContainer);
    }else{
      // It's an expense related to the company's activity
      childrenContainer = collectionView.$(collectionView.activityContainer);
    }
    this.appendChild(index, itemView, childrenContainer);
    if (_.isFunction(itemView.highlight)){
      itemView.highlight();
    }
  },
  appendChild: function(index, itemView, childrenContainer){
    childrenContainer.append(itemView.el);
  },
  onRender: function(collectionView){
    this.setTotal();
  },
  onItemRemoved: function(){
    this.setTotal();
  },
  onAfterItemAdded: function(){
    this.setTotal();
  },
  setTotal: function(){
    /*
     * Set the total value for the current collection
     */
    MyApp.vent.trigger("totalchanged");
    this.ui.internalTotal.html(formatAmount(this.collection.total('1')));
    this.ui.activityTotal.html(formatAmount(this.collection.total('2')));
  }
});


var ExpensesView = BaseExpenseCollectionView.extend({
  /*
   *  CompositeView that presents the expenses collection in a table
   */
  template: templates.expenseList,
  itemView: ExpenseLineView,
  id: "expenselines",
  ui:{
    internalTotal:'#internal_total',
    activityTotal:'#activity_total'
  },
  appendChild: function(index, itemView, childrenContainer){
    var children = childrenContainer.children();
    if (children.size() <= index) {
      childrenContainer.append(itemView.el);
    } else {
      childrenContainer.children().eq(index).before(itemView.el);
    }
  }
});


var ExpensesKmView = BaseExpenseCollectionView.extend({
  /*
   *  CompositeView that presents the expenses related to km fees in a table
   */
  template: templates.expenseKmList,
  itemView: ExpenseKmLineView,
  id:'expensekmlines',
  ui:{
    internalTotal:'#km_internal_total',
    activityTotal:'#km_activity_total'
  }
});


var BaseExpenseFormView = BaseFormView.extend({
  /*
   * Base form view
   */
  submit: Autonomie.addsubmit,
  formname: null,
  templateHelpers: function(){
    /*
     * Add datas to the template context
     */
    return {type_options:this.getTypeOptions(),
            category_options:this.getCategoryOptions()};
  },
  updateSelectOptions: function(options, val){
    /*
     * Add the selected attr to the option with value 'val'
     */
    _.each(options, function(option){
      delete option['selected'];
      if (val == option['value']){
        option['selected'] = 'true';
      }
    });
    return options;
  },
  onShow: function(){
    /*
     * Set the datepicker and its date (that need to be passed through setDate)
     */
    this.setDatePicker(this.formname, this.ui.date, "date");
  }
});


var ExpenseAdd = BaseExpenseFormView.extend({
  /*
   *  Expense add form
   */
  template: templates.expenseForm,
  formname: "expenseForm",
  // The most used UI elements
  ui:{
    form:"#expenseForm",
    date:"#expenseForm input[name=altdate]"
  },
  initialize: function(options){
    Autonomie.addFormInitialize.call(this, options);
  },
  getCategoryOptions:function(){
    /*
     * Return the options for expense categories
     */
    return AppOptions['categories'];
  },
  getTypeOptions: function(){
    /*
     *  Return the options for tva selection
     */
    return AppOptions['expensetypes'];
  }
});


var ExpenseKmAdd = BaseExpenseFormView.extend({
  /*
   * Form to add km fees expenses
   */
  template:templates.expenseKmForm,
  formname: "expenseKmForm",
  // The most used UI elements (are cached)
  ui:{
    form:"#expenseKmForm",
    date:"#expenseKmForm input[name=altdate]"
  },
  initialize: function(options){
    Autonomie.addFormInitialize.call(this, options);
  },
  getTypeOptions: function(){
    /*
     *  Return the options for tva selection
     */
    return AppOptions['kmtypes'];
  },
  getCategoryOptions:function(){
    /*
     * Return the options for expense categories
     */
    return AppOptions['categories'];
  }
});


var ExpenseEdit = ExpenseAdd.extend({
  /*
   *  Expense edit form
   */
  submit: Autonomie.editsubmit,
  initialize: function(options){
    Autonomie.editFormInitialize.call(this, options);
  },
  getCategoryOptions:function(){
    /*
     * Return the options for expense categories
     */
    var category_options = AppOptions['categories'];
    var category = this.model.get('category');
    return this.updateSelectOptions(category_options, category);

  },
  getTypeOptions: function(){
    /*
     *  Return the options for the expense types
     */
    var type_options = AppOptions['expensetypes'];
    var type_id = this.model.get('type_id');
    return this.updateSelectOptions(type_options, type_id);
  }
});


var ExpenseKmEdit = ExpenseKmAdd.extend({
  /*
   * Km expense edition
   */
  submit: Autonomie.editsubmit,
  initialize: function(options){
    Autonomie.editFormInitialize.call(this, options);
  },
  getCategoryOptions:function(){
    /*
     * Return the options for expense categories
     */
    var category_options = AppOptions['categories'];
    var category = this.model.get('category');
    return this.updateSelectOptions(category_options, category);

  },
  getTypeOptions: function(){
    var type_options = AppOptions['kmtypes'];
    var type_id = this.model.get('type_id');
    return this.updateSelectOptions(type_options, type_id);
  }
});


MyApp.Router = Backbone.Marionette.AppRouter.extend({
  /*
   *  Local route configuration
   *
   *  Link the routes to a named method that should be provided by one of the
   *  controllers
   */
  appRoutes: {
    "": "index",
    "index":"index",
    "lines/:id/edit": "edit",
    "lines/add": "add",
    "kmlines/:id/edit": "editkm",
    "kmlines/add": "addkm"
  }
});


MyApp.Controller = {
  /*
   * App controller
   */
  initialized:false,
  _popup:null,
  expense_form:null,
  expensekm_form:null,
  lines:null,
  kmlines:null,
  index: function() {
    this.ensurePopupClosed();
    this.initialize();
  },
  ensurePopupClosed: function(){
    /*
     *  ensure the popup is closed (is necessary when we come from other views)
     */
    MyApp.formContainer.close();
  },
  initialize:function(){
    if (!this.initialized){
      this.lines = new ExpensesView({collection:MyApp.expense.lines});
      this.kmlines = new ExpensesKmView( {collection:MyApp.expense.kmlines});

      MyApp.linesRegion.show(this.lines);
      MyApp.linesKmRegion.show(this.kmlines);
      this.initialized = true;
    }
  },
  _getExpenseLine:function(id){
    /*
     * Return the expenseline by id or cid
     */
    var model = MyApp.expense.lines.get(id);
    return model;
  },
  _getExpenseKmLine:function(id){
    /*
     * Return the expenseKmline by id or cid
     */
    var model = MyApp.expense.kmlines.get(id);
    return model;
  },
  add: function(){
    /*
     * expenseline add route
     */
    this.initialize();
    if (this.expense_form !== null){
      this.expense_form.reset();
    }
    this.expense_form = new ExpenseAdd({title:"Ajouter",
        modelObject:ExpenseLine,
        destCollection:MyApp.expense.lines});
    MyApp.formContainer.show(this.expense_form);
  },
  edit: function(id) {
    /*
     * expenseline edit route
     */
    this.initialize();
    if (this.expense_form !== null){
      this.expense_form.reset();
    }
    var model = this._getExpenseLine(id);
    this.expense_form = new ExpenseEdit({model:model,
                                         title:"Éditer"});
    MyApp.formContainer.show(this.expense_form);
  },
  addkm: function(){
    /*
     * expensekmline add route
     */
    this.initialize();
    if (this.expensekm_form !== null){
      this.expensekm_form.reset();
    }
    this.expensekm_form = new ExpenseKmAdd({title:"Ajouter",
    modelObject:ExpenseKmLine,
    destCollection:MyApp.expense.kmlines});
    MyApp.formContainer.show(this.expensekm_form);
  },
  editkm: function(id) {
    /*
     * expensekmline edit route
     */
    this.initialize();
    if (this.expensekm_form !== null){
      this.expensekm_form.reset();
    }
    var model = this._getExpenseKmLine(id);
    this.expensekm_form = new ExpenseKmEdit({model:model,
                                         title:"Éditer"});
    MyApp.formContainer.show(this.expensekm_form);
  }
};


MyApp.addInitializer(function(options){
  /*
   *  Application initialization
   */
  MyApp.expense = new ExpenseSheet(options['expense']);
  MyApp.router = new MyApp.Router({controller:MyApp.Controller});
});

MyApp.vent.on("totalchanged", function(){
  var text = "Total des frais professionnels à payer : ";
  var total = MyApp.expense.lines.total() +  MyApp.expense.kmlines.total();
  text += formatAmount(total);
  $('#total').html(text);
});


var pp = Popup.extend({
  el:'#form-container'
});


MyApp.addRegions({
  /*
   * Application regions
   */
  linesRegion:'#expenses',
  linesKmRegion:'#expenseskm',
  formContainer:pp
});


var ExpenseSheet = Backbone.Model.extend({
  /*
   *  Main expense sheet model
   */
  urlRoot:"/expenses/",
  initialize: function(options){
    this.lines = new ExpenseLineCollection(options['lines']);
    this.lines.url = this.urlRoot + this.id + "/lines";
    this.kmlines = new ExpenseKmCollection(options['kmlines']);
    this.kmlines.url = this.urlRoot + this.id + "/kmlines";
  }
});


$(function(){
  if (AppOptions['loadurl'] !== undefined){
    $.ajax({
      url: AppOptions['loadurl'],
      dataType: 'json',
      async: false,
      mimeType: "textPlain",
      data: {},
      success: function(data) {
        _.extend(AppOptions, data['options']);
        MyApp.start({'expense':data['expense']});
      },
      error: function(){
        alert("Une erreur a été rencontrée, contactez votre administrateur.");
      }
    });
  }else{
    alert("Une erreur a été rencontrée, contactez votre administrateur.");
  }
});
