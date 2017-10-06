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

var popup = Popup.extend({
  /*
   * Popup object that extends the default popup providing its element
   */
  el:'#form-container'
});

AutonomieApp.addRegions({
  /*
   * Application regions are used to display views
   */
  holidayRegion: "#holidays",
  formContainer: popup
});

AutonomieApp.module("Holiday", function(Holiday, AutonomieApp,  Backbone, Marionette, $, _){
  var HolidayModel = Backbone.Model.extend({
    /*
     *
     * A model representing a holiday
     */
    initialize: function(options){
      // Here we provide default values for the alt fields (alt fields are used
      // by the datepicker widget to provide a display field and a stored one
      // that will be sent to the server)
      options = options || {};

      if ( _.isUndefined( options['alt_start_date'] ) &&
           ! _.isUndefined( options['start_date'] ) ){
        this.set('alt_start_date', formatPaymentDate(options['start_date']));
      }
      if ( _.isUndefined( options['alt_end_date'] ) &&
         ! _.isUndefined( options['end_date'] ) ){
        this.set('alt_end_date', formatPaymentDate(options['end_date']));
      }
    },
    validation:{
      start_date: {
        required: true,
        pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
        msg:"est requise"
      },
      end_date: [{
        required: true,
        pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
        msg:"est requise"
      }, {fn:'check_end_date'}
      ]},
      check_end_date: function(value, attr, computedState){
        var start_date = computedState['start_date'];
        if (!_.isUndefined(start_date)){
          if (start_date > value){
            return "La date de début doit précéder celle de fin";
          }
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
    template: "holiday",
    tagName: "tr",
    events: {
      'click a.remove':'_remove',
      "click a.edit" : "_edit"
    },
    initialize: function(){
      /*
       * View constructor
       */
      // bind the model change to the view rendering
      this.listenTo(this.model, 'change', this.render, this);
    },
    _remove: function(){
      /*
       *  Delete the line
       */
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      if (confirmed){
        var _model = this.model;
        this.highlight(
        {callback: function(){_model.destroy(
          {success: function(model, response) {
            displayServerSuccess("L'élément a bien été supprimé");
          }}
        );}});
      }
    },
    _edit: function(){
      /*
       * Redirect to the edit page
       */
      var route = "edit/" + this.model.cid;
      Holiday.router.navigate(route, {trigger: true});
    },
    templateHelpers: function(){
        return {
            start_date: formatDate(this.model.start_date),
            end_date: formatDate(this.model.end_date),
        }
    }
  });
  var NoHolidatView = Backbone.Marionette.ItemView.extend({
    template: "empty"
  });
  var HolidayList = Backbone.Marionette.CompositeView.extend({
    /*
     * Holidays table
     */
    template: "holidayList",
    childViewContainer: "tbody",
    childView: HolidayView,
    emptyView: NoHolidatView,
    events: {
      "click a.add": "_add"
    },
    appendHtml: function(collectionView, childView, index){
      // Launched when an item is added to the collectionview
      // Here we provide a sorted output
      // See :
      // https://github.com/marionettejs/backbone.marionette/wiki/Adding-support-for-sorted-collections
      // for more informations
      var childrenContainer = collectionView.childViewContainer ? collectionView.$(collectionView.childViewContainer) : collectionView.$el;
      var children = childrenContainer.children();
      if (children.size() <= index) {
        childrenContainer.append(childView.el);
      } else {
        childrenContainer.children().eq(index).before(childView.el);
      }
    },
    _add: function(){
      /*
       *  Redirect our one page app to the holiday add page
       */
      Holiday.router.navigate("add", {trigger: true});
    }
  });


  var HolidayForm = BaseFormView.extend({
    /*
     *  Holiday add form view
     */
    template: "holidayForm",
    ui:{
      start_date: "#holidayForm input[name=alt_start_date]",
      end_date: "#holidayForm input[name=alt_end_date]",
      form: "#holidayForm"
    },
    onShow: function(){
      /*
       * Launched when the form is added to the dom
       * Make some js calls
       */
      this.setDatePicker("#holidayForm", this.ui.start_date, "start_date");
      this.setDatePicker("#holidayForm", this.ui.end_date, "end_date");
      this.ui.start_date.focus();
    }
  });
  var controller = {
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
      AutonomieApp.formContainer.closeModal();
    },
    initialize: function(){
      if (!this.initialized){
        this.holidays = new HolidayList({collection: Holiday.holidays});
        AutonomieApp.holidayRegion.show(this.holidays);
        this.initialized = true;
      }
    },
    add: function(){
      this.initialize();
      var model = new HolidayModel();
      holidayForm = new HolidayForm({
        title: "Ajouter",
        destCollection: Holiday.holidays,
        model:model
        });
      AutonomieApp.formContainer.show(holidayForm);
    },
    edit: function(id){
      this.initialize();
      var model = Holiday.holidays.get(id);
      holidayForm = new HolidayForm({
        title:"Éditer",
        model:model
        });
      AutonomieApp.formContainer.show(holidayForm);
    }
  };

  var router = Backbone.Marionette.AppRouter.extend({
    /*
     * Application's routes configuration
     */
    controller: controller,
    appRoutes: {
      "index": "index",
      "add": "add",
      "edit/:id": "edit"
    }
  });
  Holiday.on('start', function(){
    var options = Holiday.datas;
    Holiday.router = new router();
    Holiday.holidays = new HolidaysCollection(options['holidays']);
    Holiday.holidays.url = "/users/" + options['user_id'] + "/holidays";
    Holiday.router.controller.index();
  });
});
$(function(){
  if (AppOptions['loadurl'] !== undefined){
    var ajax_call = initLoad(AppOptions['loadurl']);
    ajax_call.then(function(datas){
      AutonomieApp.module('Holiday').datas = datas;
      AutonomieApp.start();
    });
  }
});
