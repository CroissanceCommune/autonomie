/*
 * File Name : expense.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 * The expense module handles user's expenses with models
 */
var AppOptions = {};
var MyApp = new Backbone.Marionette.Application();
MyApp.on("initialize:after", function(){
  if ((Backbone.history)&&(! Backbone.History.started)){
    Backbone.history.start();
  }
});

/******************************** Models ********************************/
var ExpenseLine = Backbone.Model.extend({
  /*
   *  Expenseline model
   */
  // default values for an expenseline
  defaults:{
    description:"",
    ht:0,
    tva:0
  },
  // Constructor dynamically add a altdate if missing
  // (altdate is used in views for jquery datepicker)
  initialize: function(options){
    if ((options!== undefined) && (options['altdate'] === undefined)){
      this.set('altdate', formatPaymentDate(options['date']));
    }
  },
  // Validation rules for our model's attributes
  validation:{
    category: {
      required:true,
      msg:"est requise"
    },
    code:{
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
      var percentage = this._getTypeOption(AppOptions['teltypes']).percentage;
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
  _getTypeOption:function(arr){
    /*
     * Retrieve the type option referenced by the current code from the passed
     * array
     */
    var code = this.get('code');
    return _.find(arr, function(type){return type['value'] === code;});
  },
  isSpecial:function(){
    /*
     * return True if this expense is a special one (related to phone)
     */
    return this._getTypeOption(AppOptions['teltypes']) !== undefined;
  },
  getTypeOption: function(){
    var arr;
    if (this.isSpecial()){
      arr = AppOptions['teltypes'];
    }else{
      arr = AppOptions['expensetypes'];
    }
    return this._getTypeOption(arr);
  },
  getTypeLabel: function(){
    /*
     * Return the Label of the current type
     */
    var option = this.getTypeOption();
    if (option === undefined){
      return "";
    }else{
      return option.label;
    }
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


var ExpenseKmLine = Backbone.Model.extend({
  /*
   *  Model for expenses related to kilometers fees
   */
  defaults:{
    start:"",
    end:"",
    description:""
  },
  initialize: function(options){
    if (options['altdate'] === undefined){
      this.set('altdate', formatPaymentDate(options['date']));
    }
  },
  validation:{
    code:{
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
    var elem = _.where(AppOptions['kmtypes'], {value:this.get('code')})[0];
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
  }
});


var ExpenseKmCollection = Backbone.Collection.extend({
  /*
   * Collection for expenses related to km fees
   */
  model: ExpenseKmLine,
  total: function(){
    var result = 0;
    this.each(function(model){
      result += model.total();
    });
    return result;
  }
});


/********************  Views  *********************************/
var ExpenseLineView = Backbone.Marionette.ItemView.extend({
  /*
   *  table row view
   */
  template: templates.expense,
  tagName:"tr",
  televents: {
    'click a.remove':'_remove',
    'change input[name=ht]':'changeVal',
    'change input[name=tva]':'changeVal'
  },
  telui:{
    htinput:'input[name=ht]',
    tvainput:'input[name=tva]'
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
            total:formatAmount(total)};
  },
  initialize: function(){
    /*
     * View constructor
     */
    // bind the model change to the view rendering
    this.listenTo(this.model, 'change', this.render, this);
    if (this.model.isSpecial()){
      this.template = templates.expensetel;
      this.ui = this.telui;
      this.events = this.televents;
      // TODO : bind input change events here to avoid js warnings
    }
  },
  changeVal: function(){
    Backbone.Validation.bind(this);
    var this_ = this;
    this.model.save({
            ht:this.ui.htinput.val(),
            tva:this.ui.tvainput.val()
            }, {
            success:function(){
              console.log("Success Val");
              this_.highlight();
            },
            wait:true});
    Backbone.Validation.unbind(this);

  },
  onRender:function(){
    this.highlight();
  },
  _remove: function(){
    /*
     *  Delete the line
     */
    var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
    if (confirmed){
      var _model = this.model;
      this.highlight(function(){_model.destroy();});
    }
  },
  highlight: function( callback ){
    /*
     * Ok highlight
     */
    this._highlight("#ceff99", callback);
  },
  error: function(callback){
    /*
     * Error highlight
     */
    this._highlight("#F9AAAA", callback);
  },
  _highlight: function(color, callback){
    var top = this.$el.offset().top - 50;
    $('html, body').animate({scrollTop: top});
    this.$el.effect('highlight', {color:color}, 1500,
                    function(){if (callback !== undefined){ callback();}
                });
  }
});


var ExpensesView = Backbone.Marionette.CompositeView.extend({
  /*
   *  CompositeView that presents the expenses collection in a table
   */
  template: templates.expenseList,
  itemView: ExpenseLineView,
  tagName: "div",
  id: "expenselines",
  internalContainer: "tbody.internal",
  activityContainer: "tbody.activity",
  ui:{
    internalTotal:'#internal_total',
    activityTotal:'#activity_total'
  },
  appendHtml: function(collectionView, itemView, index){
    /*
     *  Ensure the item is appended in the right order
     */
    var childrenContainer;
    if (itemView.model.get('category') == '1'){
      // It's an expense related to internal needs
      childrenContainer = collectionView.$(collectionView.internalContainer);
    }else{
      // It's an expense related to the company's activity
      childrenContainer = collectionView.$(collectionView.activityContainer);
    }
    var children = childrenContainer.children();
    if (children.size() <= index) {
      childrenContainer.append(itemView.el);
    } else {
      childrenContainer.children().eq(index).before(itemView.el);
    }
  },
  onRender: function(collectionView){
    this.ui.internalTotal.html(formatAmount(this.collection.total('1')));
    this.ui.activityTotal.html(formatAmount(this.collection.total('2')));
  }
});


var ExpenseKmLineView = Backbone.Marionette.ItemView.extend({
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
    var code = this.model.get('code');
    var selected_type = _.where(AppOptions['kmtypes'], {value:String(code)});
    var total = this.model.total();
    var edit_url = "#kmlines/" + this.model.cid + "/edit";
    return {typelabel:selected_type[0]['label'],
            edit_url:edit_url,
            total:formatAmount(total)};
  },
  initialize: function(){
    this.listenTo(this.model, 'change', this.render, this);
  }
});


var ExpensesKmView = Backbone.Marionette.CompositeView.extend({
  /*
   *  CompositeView that presents the expenses related to km fees in a table
   */
  template: templates.expenseKmList,
  itemView: ExpenseKmLineView,
  className:"table table-bordered table-condensed table-disable-hover",
  tagName: "table",
  childrenContainer: "tbody",
  ui: {
    total: '#km_total'
  },
  onRender:function(collectionView){
    this.ui.total.html(formatAmount(collectionView.collection.total()));
  },
  onAfterItemAdded: function(view){
    console.log("Item added");
    view.highlight();
  }

});


var BaseFormView = Backbone.Marionette.CompositeView.extend({
  /*
   * Base form view
   */
  dateAltField:null,
  isClosed:false,
  initialize: function(options){
    var that = this;
    this.isClosed = false;
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
    this.ui.date.datepicker({
          altField:this.dateAltField,
          altFormat:"yy-mm-dd",
          dateFormat:"dd/mm/yy"
          });
      var date = this.model.get('date');
      if ((date !== null) && (date !== undefined)){
        date = parseDate(date);
        this.ui.date.datepicker('setDate', date);
      }
  },
  onBeforeClose:function(){
    this.reset();
  },
  onClose:function(){
    MyApp.router.navigate("index", {trigger: true});
  },
  reset:function(){
    /*
     *  Reset the form (set all fields to blank)
     */
    resetForm(this.ui.form);
  }
});


var ExpenseKmAdd = BaseFormView.extend({
  /*
   * Form to add km fees expenses
   */
  events: {
    'click button[name=submit]':'submit',
    'click button[name=cancel]':'close'
  },
  template:templates.expenseKmForm,
  dateAltField:"#expenseKmForm input[name=date]",
  // The most used UI elements
  ui:{
    form:"#expenseKmForm",
    date:"#expenseKmForm input[name=altdate]"
  },
  templateHelpers: function(){
    var type_options = this.getTypeOptions();
    return {type_options:type_options};
  },
  getTypeOptions: function(){
    /*
     *  Return the options for tva selection
     */
    return AppOptions['kmtypes'];
  },
  submit: function(e){
    /*
     *  Handle form submission
     */
    e.preventDefault();
    var data = this.ui.form.serializeObject();
    this.model = new ExpenseKmLine(data);
    this.model.urlRoot = MyApp.expense.kmlines.url;
    // We bind the view and its model to Backbone.Validation
    Backbone.Validation.bind(this);
    var this_ = this;
    this.model.save(data,
                      {error:function(model, xhr, options){
                        console.log("error");
                        //TODO
                        Backbone.Validation.unbind(this_);
                      },
                      success:function(model, response, options){
                        MyApp.expense.kmlines.add(model);
                      },
                      wait:true
                    });
  }
});

var ExpenseKmEdit = BaseFormView.extend({
  /*
   *
   */
  getTypeOptions: function(){
    var type_options = AppOptions['kmtypes'];
    var code = this.model.get('code');
    return this.updateSelectOptions(type_options, type_);
  },
  submit: function(e){
    e.preventDefault();
    var data = this.ui.form.serializeObject();
    var this_ = this;
    this.model.save(data,
              {error:function(model, xhr, options){
                console.log("error");
              },
              success:function(model, response, options){
                this_.close();
              },
              wait:true
              }
        );
  }
});

var ExpenseAdd = BaseFormView.extend({
  /*
   *  Expense add form
   */
  template: templates.expenseForm,
  dateAltField:"#expenseForm input[name=date]",
  events: {
    'click button[name=submit]':'submit',
    'click button[name=cancel]':'close'
  },
  // The most used UI elements
  ui:{
    form:"#expenseForm",
    date:"#expenseForm input[name=altdate]"
  },
  initialize: function(options){
    this.destCollection = options['destCollection'];
    this.modelObject = options['modelObject'];
    this.model = new this.modelObject();
    Backbone.Validation.bind(this);
  },
  templateHelpers: function(){
    /*
     * return custom elements for rendering
     */
    var type_options = this.getTypeOptions();
    var category_options = this.getCategoryOptions();
    var options =  {type_options:type_options,
                    category_options:category_options};
    return options;
  },
  getCategoryOptions:function(){
    /*
     * Return the options for expense categories
     */
    return AppOptions['expensecategories'];
  },
  getTypeOptions: function(){
    /*
     *  Return the options for tva selection
     */
    return AppOptions['expensetypes'];
  },
  submit: function(e){
    /*
     *  Handle form submission
     */
    e.preventDefault();
    var this_ = this;
    var data = this.ui.form.serializeObject();
    this.destCollection.create(data,
      { success:function(){
          this_.close();
         },
        error: function(){
          console.log("Error");
        },
        wait:true,
        sort:true}
    );
  }
});


var ExpenseEdit = ExpenseAdd.extend({
  /*
   *  Expense edit form
   */
  initialize:function(){
    // bind model validation to our view (and its model)
    Backbone.Validation.bind(this);
  },
  getCategoryOptions:function(){
    /*
     * Return the options for expense categories
     */
    var category_options = AppOptions['expensecategories'];
    var category = this.model.get('category');
    return this.updateSelectOptions(category_options, category);

  },
  getTypeOptions: function(){
    /*
     *  Return the options for the expense types
     */
    var type_options = AppOptions['expensetypes'];
    var code = this.model.get('code');
    return this.updateSelectOptions(type_options, code);
  },
  submit: function(e){
    /*
     * submit the edition form
     */
    var collection = this.model.collection;
    e.preventDefault();
    var this_ = this;
    var data = this.ui.form.serializeObject();
    this.model.save(data, {
      success:function(){
        collection.remove(this_.model);
        collection.add(this_.model);
        this_.close();
      },
      wait:true
    });
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
      var collectionView = new ExpensesView({collection:MyApp.expense.lines});
      var collectionKmView = new ExpensesKmView(
                                          {collection:MyApp.expense.kmlines});

      MyApp.linesRegion.show(collectionView);
      MyApp.linesKmRegion.show(collectionKmView);
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
        modelObject:ExpenseLine, destCollection:MyApp.expense.lines});
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
    this.expensekm_form = new ExpenseKmAdd({title:"Ajouter"});
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
    this.lines.url = this.urlRoot + this.id + "/lines/";
    this.kmlines = new ExpenseKmCollection(options['kmlines']);
    this.kmlines.url = this.urlRoot + this.id + "/kmlines/";
  }
});


$(function(){
  if (AppOptions['expense'] !== undefined){
    MyApp.start({'expense':AppOptions['expense']});
  }else{
    alert("Une erreur a été rencontrée, contactez votre administrateur.");
  }
});
