/*
 * File Name : statistics.js
 *
 * Copyright (C) 2015 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */


/*
 *
 * 1- page stats : sheet + list of entries + add button
 *
 * 2- entry form : entry + criteria + add button
 *
 * 3- criterion form : criterion
 *
 * on entry modify :
 *  load criteria
 *  create collection
 *
 *  show layout
 *  show list
 *  add button behaviour
 *
 * on criterion modify
 *
 *
 */
var AppOptions = {};
var pp = Popup.extend({
  el:'#popup_container'
});

AutonomieApp.addRegions({
  sheet: "#sheet",
  entries: '#entrylist',
  entry_edit: "#entry_edit",
  popup: pp
});

AutonomieApp.module('Statistic', function(Statistic, App, Backbone, Marionette, $, _){
  var EntryFormLayout = Marionette.LayoutView.extend({
    template: "full_entry_form",
    events: {
      'click button.close': "closeView"
    },
    ui: {
      title: 'h4'
    },
    regions: {
      list: '#criteria',
      form: '#criterion-form'
    },
    closeView: function(){
      this.destroy();
      AutonomieApp.router.navigate("index", {trigger: true});
    },
    focus: function(){
      $('html, body').animate(
      {scrollTop: this.ui.title.offset().top}, 2000);
    }
  });
  var SheetModel = Backbone.Model.extend({
    validation:{
      title: {
        required:true,
        msg:"est requis"
      }
    }
  });
  var EntryModel = Backbone.Model.extend({
    defaults: {criterion: []},
    validation:{
      title: {
        required:true,
        msg:"est requis"
      }
    },
    csv_url: function(){
      return this.url() + "?format=csv";
    }  });
  var EntryCollection = Backbone.Collection.extend({
    model: EntryModel
  });
  var EntryView = BaseTableLineView.extend({
    template: "entry",
    tagName: "tr",
    events: {
      'click a.remove':'_remove'
    },
    templateHelpers: function(){
      return {csv_url: this.model.csv_url()};
    },
    modelEvents:{
      "change:title": "render"
    },
    _remove: function(id){
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      if (confirmed){
        var _model = this.model;
        this.highlight({
          callback: function(){
            _model.destroy({
                success: function(model, response) {
                  Statistic.router.navigate("index", {trigger: true});
                  displayServerSuccess("L'élément a bien été supprimé");
                }
             });
           }
          });
      }
    }
  });
  var EntryListView = Marionette.CompositeView.extend({
    childView: EntryView,
    template: "entry_list",
    childViewContainer: 'tbody'
  });
  var EntryFormView = BaseFormView.extend({
    template: "entry_form",
    ui: {
      form: "form"
    },
    focus: function(){
      this.ui.form.find('input').first().focus();
    },
    closeView: function(result){
      if (!_.isUndefined(result)){
        if (!_.isUndefined(result.id)){
          this.destroy();
          Statistic.router.navigate("entries/" + result.id + "/edit" ,
          {trigger: true});
          return;
        }
      }
      this.destroy();
      AutonomieApp.router.navigate("index", {trigger: true});
      return;
    }
  });
  var CriterionView = Marionette.ItemView.extend({
    template: "criterion",
    tagName: 'tr'
  });
  var CriteriaListView = Marionette.CompositeView.extend({
    childView: CriterionView,
    template: "criterion_list",
    childViewContainer: 'tbody'
  });
  var SheetView = Marionette.ItemView.extend({
    model: SheetModel,
    template: "sheet_form",
    ui: {
      form: 'form'
    },
    events: {
      "click button.edit": "toggleForm",
      "click button.submit": "changeTitle",
      "submit form": "changeTitle"
    },
    formDatas: function(){
      return this.ui.form.serializeObject();
    },
    toggleForm: function(){
      this.ui.form.toggle();
    },
    changeTitle: function(event){
      Backbone.Validation.bind(this);
      event.preventDefault();
      this.model.save(
        this.formDatas(),
        {
          success: function(){
            displayServerSuccess("Vos données ont été sauvegardées");
          },
          error:function(model, xhr, options){
            displayServerError("Une erreur a été rencontrée lors de la " +
                "sauvegarde de vos données");
          }
        }
      );
      Backbone.Validation.unbind(this);
      this.render();
      return true;
    }
  });
  var controller = {
    initialized:false,
    index: function(){
      this.initialize();
      App.popup.empty();
      App.entry_edit.empty();
    },
    initialize: function(){
      if (! this.initialized){
        this.sheet_view = new SheetView({model: Statistic.sheet});
        App.sheet.show(this.sheet_view);
        this.entry_list_view = new EntryListView(
          {collection: Statistic.entries}
        );
        App.entries.show(this.entry_list_view);
      }
    },
    entry_add: function(){
      this.initialize();
      var model = new EntryModel({});
      var entry_form = new EntryFormView({
        model: model, destCollection: Statistic.entries
      });
      App.popup.show(entry_form);
    },
    entry_edit: function(id){
      this.initialize();
      var model = Statistic.entries.get(id);
      var entry_form = new EntryFormLayout({
        model: model,
        destCollection: Statistic.entries
      });
      var criteria = model.criteria;
      var criteria_collection = new Backbone.Collection(criteria);
      var criteria_list = new CriteriaListView({collection: criteria_collection});
      App.entry_edit.show(entry_form);
      entry_form.focus();
      entry_form.getRegion('list').show(criteria_list);
    }
  };
  router = Backbone.Marionette.AppRouter.extend({
    controller: controller,
    appRoutes: {
      "index": "index",
      "entries/:id/edit": "entry_edit",
      "entries/add": "entry_add"
    }
  });
  Statistic.on('start', function(){
    var data = Statistic.datas;
    Statistic.router = new router();
    Statistic.sheet = new SheetModel(data['sheet']);
    Statistic.sheet.url = AppOptions['sheet_edit_url'];
    Statistic.entries = new EntryCollection(data['entries']);
    Statistic.entries.url = AppOptions['entry_root_url'];
    Statistic.router.controller.index();
  });
});



function StatisticPageInit(options){
  if (AppOptions['loadurl'] !== undefined){
    // page statistic
    var module = AutonomieApp.module('Statistic');
    // Quand on start on lance initModule en callback de la requête jquery
    var options_load = initLoad(AppOptions['loadurl']).then(
      function(data){
        _.extend(AppOptions, data);
      }
    );
    var sheet_load = initLoad(AppOptions['contexturl']);
    sheet_load.then(function(datas){
      module.datas = datas;
    });
    $.when(options_load, sheet_load).then(
      function(datas){
        AutonomieApp.start();
      }
    );
  }
}

function StatisticsPageInit(options){
  if (AppOptions['submiturl'] !== undefined){
    var form_container = $('#form-container');
    var sheet_form = Handlebars.templates['sheet_form.mustache']();
    form_container.html(sheet_form);
    var input = form_container.find('input');
    var submit_button = form_container.find('button.submit');
    $('button.btn-add').on('click', function(){
      form_container.fadeIn();
    });
    submit_button.on("click", function(event){
      event.preventDefault();
      var title = input.val();
      if (title.length === 0){
        showError(input, "Requis");
      } else {
        hideFormError(form_container);
        $.ajax({
          url: AppOptions['submiturl'],
          method: 'POST',
          dataType: 'json',
          data: {title: title},
          success: function(result){
          }
        });
      }
    });
  }
}

$(function(){
  StatisticPageInit();
  StatisticsPageInit();
});
