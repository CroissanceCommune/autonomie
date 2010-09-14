/*
 * File Name : holiday.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
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


var HolidayModel = Backbone.Model.extend({
  /*
   *
   * A model representing a holiday
   */
  initialize: function(options){
    // Here we provide default values for the alt fields (alt fields are used
    // by the datepicker widget to provide a display field and a stored one
    // that will be sent to the server)
    if ((options['alt_start_date'] === undefined)&&(options['start_date']!==undefined)){
      this.set('alt_start_date', formatPaymentDate(options['start_date']));
    }
    if ((options['alt_end_date'] === undefined)&&(options['end_date']!==undefined)){
      this.set('alt_end_date', formatPaymentDate(options['end_date']));
    }
  },
  validation:{
    start_date: {
      required: true,
      pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
      msg:"est requise"
    },
    end_date: {
      required: true,
      pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
      msg:"est requise"

    }
  }
});


var HolidaysCollection = Backbone.Collection.extend({
  /*
   *  A collection of holidays sorted by start date
   */
  model: HolidayModel,
  comparator: function(model){
    return model.get('start_date');
  }
});


var HolidayView = BaseTableLineView.extend({
  /*
   * A single line in the table
   */
  template: templates.holiday,
  tagName: "tr",
  events: {
    'click a.remove':'_remove',
    "click a.edit" : "_edit"
  },
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
  },
  _edit: function(){
    /*
     * Redirect to the edit page
     */
    var route = "edit/" + this.model.cid;
    MyApp.router.navigate(route, {trigger: true});
  }
});

var HolidayList = Backbone.Marionette.CompositeView.extend({
  /*
   * Holidays table
   */
  template: templates.holidayList,
  itemViewContainer: "tbody",
  itemView: HolidayView,
  events: {
    "click a.add": "_add"
  },
  appendHtml: function(collectionView, itemView, index){
    // Launched when an item is added to the collectionview
    // Here we provide a sorted output
    // See :
    // https://github.com/marionettejs/backbone.marionette/wiki/Adding-support-for-sorted-collections
    // for more informations
    var childrenContainer = collectionView.itemViewContainer ? collectionView.$(collectionView.itemViewContainer) : collectionView.$el;
    var children = childrenContainer.children();
    if (children.size() <= index) {
      childrenContainer.append(itemView.el);
    } else {
      childrenContainer.children().eq(index).before(itemView.el);
    }
  },
  _add: function(){
    /*
     *  Redirect our one page app to the holiday add page
     */
    MyApp.router.navigate("add", {trigger: true});
  }
});


var HolidayAdd = BaseFormView.extend({
  /*
   *  Holiday add form view
   */
  template: templates.holidayForm,
  ui:{
    start_date: "#holidayForm input[name=alt_start_date]",
    end_date: "#holidayForm input[name=alt_end_date]",
    form: "#holidayForm"
  },
  submit: Autonomie.addsubmit,
  initialize: function(options){
    Autonomie.addFormInitialize.call(this, options);
  },
  onShow: function(){
    /*
     * Launched when the form is added to the dom
     * Make some js calls
     */
    this.setDatePicker("holidayForm", this.ui.start_date, "start_date");
    this.setDatePicker("holidayForm", this.ui.end_date, "end_date");
  }
});


var HolidayEdit = HolidayAdd.extend({
  /*
   * Holiday edition form
   */
  submit: Autonomie.editsubmit,
  initialize: function(options){
    Autonomie.editFormInitialize.call(this, options);
  }
});


MyApp.Controller = {
  /*
   * Application controller
   * Provides methods that are called regarding the router's configuration
   */
  holidays: null,
  addform: null,
  editform: null,
  initialized: false,
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
  initialize: function(){
    if (!this.initialized){
      this.holidays = new HolidayList({collection: MyApp.holidays});
      MyApp.holidayRegion.show(this.holidays);
      this.initialized = true;
    }
  },
  add: function(){
    this.initialize();
    if (this.addform !== null){
      this.addform.reset();
    }
    this.addform = new HolidayAdd({'title': "Ajouter",
      modelObject: HolidayModel,
      destCollection:MyApp.holidays});
    MyApp.formContainer.show(this.addform);
  },
  edit: function(id){
    this.initialize();
    if (this.editform !== null){
      this.editform.reset();
    }
    model = MyApp.holidays.get(id);
    this.editform = new HolidayEdit({model:model, title:"Éditer"});
    MyApp.formContainer.show(this.editform);
  }
};


MyApp.Router = Backbone.Marionette.AppRouter.extend({
  /*
   * Application's routes configuration
   */
  appRoutes: {
    "": "index",
    "index": "index",
    "add": "add",
    "edit/:id": "edit"
  }
});


var popup = Popup.extend({
  /*
   * Popup object that extends the default popup providing its element
   */
  el:'#form-container'
});

MyApp.addRegions({
  /*
   * Application regions are used to display views
   */
  holidayRegion: "#holidays",
  formContainer: popup
});


MyApp.addInitializer(function(options){
  /*
   *  Application initialization
   *  options : data provided by the server on setup ajax call
   *
   *  options should provide : a holidays objects list and a user_id param
   */
  MyApp.holidays = new HolidaysCollection(options['holidays']);
  MyApp.holidays.url = "/user/" + options['user_id'] + "/holidays";
  MyApp.router = new MyApp.Router({controller: MyApp.Controller});
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
        MyApp.start(data);
      },
      error: function(){
        alert("Une erreur a été rencontrée, contactez votre administrateur.");
      }
    });
  }else{
    alert("Une erreur a été rencontrée, contactez votre administrateur.");
  }
});
