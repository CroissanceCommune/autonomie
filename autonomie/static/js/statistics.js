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

/*
 *
 *  TODOLIST :
 *
 *  - popup redirect on criterion add ... :
 *      solution : ajoute une région popup au layout
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

  var get_edit_url = function(model){
    /*
     * Returns the edit url for a given model
     */
    var entry_id = model.get('entry_id');
    if (_.isUndefined(entry_id)){
      entry_id = model.collection.entry_id;
    }
    return "entries/" +
      entry_id +
      "/criteria/" +
      model.get('id') +
      "/edit";
  };

  var EntryFormLayout = Marionette.LayoutView.extend({
    template: "full_entry_form",
    events: {
      'click #entry_list_header button.close': "toggleForm",
      'click #entry_list_header button.back-btn': "closeView",
      'click #entry_list_header button.edit': "toggleForm",
      "click #entry_edit_form button[name=submit]": "changeDatas",
      "submit form": "changeDatas",
      "click #entry_edit_form button[name=cancel]": "toggleForm",
      'click button.csv_export': '_open_csv_popup'
    },
    modelEvents: {
      change: "updateDatas"
    },
    ui: {
      title: '#entry_list_header h4 span',
      form: '#entry_edit_form',
      description: "#entry_list_header span.help-block"
    },
    regions: {
      list: '#criteria',
      form: '#criterion-form'
    },
    closeView: function(){
      var this_ = this;
      this.$el.slideUp(400, function(){
        this_.destroy();
        AutonomieApp.router.navigate("index", {trigger: true});
      });
    },
    focus: function(){
      $('html, body').animate(
      {scrollTop: this.ui.title.offset().top}, 650);
    },
    formDatas: function(){
      return this.ui.form.serializeObject();
    },
    toggleForm: function(){
      this.ui.form.toggle();
    },
    updateDatas: function(){
      this.ui.title.html(this.model.get('title'));
      this.ui.description.html(this.model.get('description'));
    },
    changeDatas: function(event){
      Backbone.Validation.bind(this);
      event.preventDefault();
      var this_ = this;
      this.model.save(
        this.formDatas(),
        {
          success: function(){
            displayServerSuccess("Vos données ont été sauvegardées");
            this_.toggleForm();
          },
          error:function(model, xhr, options){
            displayServerError("Une erreur a été rencontrée lors de la " +
                "sauvegarde de vos données");
          },
          wait: true
        }
      );
      Backbone.Validation.unbind(this);
      return true;
    },
    _open_csv_popup: function(){
        var csv_url = this.model.csv_url();
        openPopup(csv_url, this.model.title);
    }
  });

  var SheetModel = Backbone.Model.extend({
    validation:{
      title: {
        required:true,
        msg:"est requis"
      }
    },
    csv_url: function(){
      var param_index = this.url.indexOf('?');
      var root_url = this.url;
      if (param_index > 0){
        root_url = this.url.substring(0, param_index);
      }
      return root_url + "?format=csv";
    }
  });

  var EntryModel = Backbone.Model.extend({
    defaults: {criteria: []},
    validation:{
      title: {
        required:true,
        msg:"est requis"
      }
    },
    csv_url: function(){
      return this.url() + "?format=csv";
    },
    criteria_url: function(){
      return this.url() + "/criteria";
    }
  });

  var EntryCollection = Backbone.Collection.extend({
    model: EntryModel
  });

  var CriterionModel = Backbone.Model.extend({
    defaults: {
      criteria: []
    },
    validation: {
      criteria: function(value){
        if ((this.get('type') == 'or') || (this.get('type') == 'and')){
          if (value.length === 0){
            return "Sélectionnez au moins une entrée";
          }
        }
      }
    },
    initialize: function(options){
      if ((this.get('type') == 'date') || (this.get('type') == 'multidate')){
        this.setDateAttributes(options);
      }
    },
    setDateAttributes: function(options){
      if ((options['altdate1'] === undefined)&&(options['search1']!==undefined)){
        this.set('altdate1', formatPaymentDate(options['search1']));
      }
      if ((options['altdate2'] === undefined)&&(options['search2']!==undefined)){
        this.set('altdate2', formatPaymentDate(options['search2']));
      }
    },
    get_subcriteria_label: function(criteria, app_options){
      var label = '';
      _.each(criteria, function(model_dict){
        var m = new CriterionModel(model_dict);
        label += "<li>";
        label += m.get_full_label(AppOptions);
        label += "<a href='#" + get_edit_url(m) + "'>Modifier</a>";
        label += "</li>";
      });
      return label;
    },
    get_or_label: function(app_options){
      var label = "Clause OU <ul>";
      label += this.get_subcriteria_label(this.get('criteria'));
      label += '</ul>';
      return label;
    },
    get_and_label: function(app_options){
      var label = "Clause ET <ul>";
      label += this.get_subcriteria_label(this.get('criteria'));
      label += "</ul>";
      return label;
    },
    get_full_label: function(app_options){
      var label;
      if (this.get('type') == 'or'){
        return this.get_or_label(app_options);
      }
      if (this.get('type') == 'and'){
        return this.get_and_label(app_options);
      }
      var title = app_options.columns[this.get('key')].label;
      var type = this.get('type');
      var labels;
      var key;
      var options;
      if((type == 'date') || (type == 'multidate')){
        labels = [this.get('altdate1'), this.get('altdate2')];
      } else if (type == 'optrel') {
        key = this.get('key');
        options = app_options.optrel_options[key];
        labels = getLabels(options, this.get('searches'));
      } else if( type == 'static_opt') {
        key = this.get('key');
        options = app_options.static_opt_options[key];
        labels = getLabels(options, this.get('searches'));
      } else if (type == 'bool') {
        labels = [];
      }
      else {
        labels = [this.get('search1'), this.get('search2')];
      }
      label = labels.join(' - ');

      if (label === ' - '){
        label = '';
      }else if (label.indexOf('- ', label.length - 2) != -1){
        label = label.substring(0, label.length - 2);
      }

      var type_methods = app_options.methods[type];
      var model_method = this.get('method');
      var method_label;
      var method = _.find(type_methods,
        function(method){ return method.value==model_method;}
      );
      if (!_.isUndefined(method)){
        method_label = method.label;
      } else {
        method_label = "Erreur";
      }

      final_label = title + " ( " + method_label;
      if (label !== ''){
        final_label += ' : ' + label;
      }
      final_label += ' )';

      return final_label;
    }
  });

  var CriteriaCollection = Backbone.Collection.extend({
    model: CriterionModel,
    initialize: function(options){
      this.url = options.url;
      this.entry_id = options.entry_id;
    }
  });

  var EntryView = BaseTableLineView.extend({
    template: "entry",
    tagName: "tr",
    events: {
      'click a.remove':'_remove',
      'click button.csv_export': '_open_csv_popup'
    },
    _open_csv_popup: function(){
        var csv_url = this.model.csv_url();
        openPopup(csv_url, this.model.title);
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
                  this_.destroy();
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
    childViewContainer: 'tbody',
    fadeIn: function(){
      if (! this.$el.is(':visible')) {
        this.$el.slideDown();
      }
    },
    fadeOut: function(){
      if (this.$el.is(':visible')) {
        this.$el.slideUp();
      }
    }
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

  var CriterionTypeSelectView = Marionette.ItemView.extend({
    /*
     * View for criterion type selection
     */
    initialize: function(options){
      this.add_url = options.add_url;
    },
    template: 'criterion_type_select',
    templateHelpers: function(){
      return {columns: _.values(AppOptions.columns)};
    },
    ui: {
      select: 'select'
    },
    events: {
      'click button[name=submit]':'onFormSubmit',
      'click button[name=cancel]':'closeView'
    },
    onFormSubmit: function(event){
      event.preventDefault();
      var selected = this.ui.select.children('option:selected');
      var key = selected.val();
      Statistic.router.navigate(this.add_url + key, {trigger: true});
      this.closeView();
    },
    closeView: function(){
      this.destroy();
    }
  });

  var getLabels = function(options, ids){
      /*
       * Get the labels of a list options matching and ids list
       */
      var selected = _.filter(
        options,
        function(option){
          return _.contains(ids, option.value);
        }
      );
      return _.pluck(selected, 'label');
  };

  var CriterionView = BaseTableLineView.extend({
    template: "criterion",
    tagName: 'tr',
    modelEvents:{
      "change": "render"
    },
    events: {
      'click a.remove':'_remove'
    },
    _remove: function(id){
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      var this_ = this;
      if (confirmed){
        var _model = this.model;
        this.highlight({
          callback: function(){
            _model.destroy({
                success: function(model, response) {
                  this_.destroy();
                  displayServerSuccess("L'élément a bien été supprimé");
                }
             });
           }
          });
      }
    },
    templateHelpers: function(){
      var result = {
        model_label: this.model.get_full_label(AppOptions),
        edit_url: get_edit_url(this.model)
      };

      return result;
    }
  });

  var CriteriaListView = Marionette.CompositeView.extend({
    childView: CriterionView,
    template: "criterion_list",
    childViewContainer: 'tbody',
    events: {
      "click a.add": "dialogCriterionType",
      "click a.add-or": "addOrCriterion",
      "click a.add-and": "addAndCriterion"
    },
    dialogCriterionType: function(){
      var add_url = "entries/" + this.collection.entry_id + "/criteria/add/";
      var criterion_type_select = new CriterionTypeSelectView(
        {add_url: add_url}
      );
      App.popup.show(criterion_type_select);
    },
    addOrCriterion: function(){
      var url = "entries/" + this.collection.entry_id + "/orcriteria/add";
      Statistic.router.navigate(url, {trigger: true});
    },
    addAndCriterion: function(){
      var url = "entries/" + this.collection.entry_id + "/andcriteria/add";
      Statistic.router.navigate(url, {trigger: true});
    },
    filter: function(child, index, collection){
      return child.get('parent_id') === null;
    }
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
    },
    templateHelpers: function(){
      return {csv_url: this.model.csv_url()};
    }
  });
  var BaseCriterionFormView = BaseFormView.extend({
    formselector: "form[name=criterion]",
    events:{
      'click button.close': "closeView",
      'click button[name=submit]':'onFormSubmit',
      'click button[name=cancel]':'closeView',
      'submit form': 'onFormSubmit'
    },
    ui:{
      "form": "form[name=criterion]"
    },
    templateHelpers: function(){
      var type = this.model.get('type');
      var key = this.model.get('key');
      var method_options = AppOptions.methods[type];
      var method = this.model.get('method');
      method_options = this.updateSelectOptions(method_options, method);
      return {
        label: AppOptions.columns[this.model.get('key')].label,
        method_options: method_options
      };
    },
    closeView: function(){
      Statistic.router.navigate("entries/" + this.destCollection.entry_id + "/edit" ,
      {trigger: true});
      this.destroy();
      return;
    }
  });
  var DateCriterionFormView = BaseCriterionFormView.extend({
    template: "datecriterion_form",
    ui:{
      "form": "form[name=criterion]",
      "search1": "input[name=altdate1]",
      "search2": "input[name=altdate2]"
    },
    onShow: function(){
       //Called when added to the DOM by the région
      this.setDatePicker(this.formselector, this.ui.search1, "search1");
      this.setDatePicker(this.formselector, this.ui.search2, "search2");
    },
    onRender: function(){
      // Called when rendered (the first time the setDatePicker doesn't work
      // because the datas is rendered but not added to the DOM, that's why the
      // call is also made in onShow)
      this.setDatePicker(this.formselector, this.ui.search1, "search1");
      this.setDatePicker(this.formselector, this.ui.search2, "search2");
    }
  });

  var StringCriterionView = BaseCriterionFormView.extend({
    template: "stringcriterion_form"
  });

  var BoolCriterionView = BaseCriterionFormView.extend({
    template: "boolcriterion_form"
  });

  var NumberCriterionView = BaseCriterionFormView.extend({
    template: "numbercriterion_form"
  });

  var OptRelCriterionForm = BaseCriterionFormView.extend({
    template: "optrelcriterion_form",
    ui:{
      "form": "form[name=criterion]",
      "select": "form[name=criterion] select"
    },
    templateHelpers: function(){
      var result = BaseCriterionFormView.prototype.templateHelpers.call(this);
      var searches = this.model.get('searches');
      optrel_options = this.updateSelectOptions(this.optrel_options, searches);
      result.optrel_options = optrel_options;
      return result;
    },
    onShow: function(){
      this.ui.select.select2();
    },
    onRender: function(){
      this.ui.select.select2();
    }
  });

  var CombinedCriterionForm = BaseCriterionFormView.extend({
    ui:{
      "form": "form[name=criterion]",
      "select": "form[name=criterion] select"
    },
    templateHelpers: function(){
      var type = this.model.get('type');
      var criteria_options = [];
      var selected_criteria_ids = [];

      /* Collect selected criteria */
      _.each(this.model.get('criteria'), function(datas){
        if (_.isObject(datas)){
          var model = new CriterionModel(datas);
          criteria_options.push(
            {
              value: model.get('id'),
              label: model.get_full_label(AppOptions),
              selected: true}
          );
          selected_criteria_ids.push(model.get('id'));
        }
      });
      _.each(this.destCollection.models, function(model){
        if ((model.get('type') != 'or') && (model.get('type') != 'and') ){
          if (!_.contains(selected_criteria_ids, model.get('id'))){
              criteria_options.push(
                {
                  value: model.get('id'),
                  label: model.get_full_label(AppOptions)
                }
              );
          }
        }
        }
      );
      return {
        type: type,
        label: this.label,
        criteria_options: criteria_options
        };
    },
    onShow: function(){
      this.ui.select.select2();
    },
    onRender: function(){
      this.ui.select.select2();
    },
    formDatas: function(){
      var result = this.ui.form.serializeObject();
      if (!('criteria' in result)){
        result['criteria'] = [];
      }
      return result;
    }
  });
  var OrCriterionForm = CombinedCriterionForm.extend({
    template: "orcriterion_form",
    label: "Configuration d'une clause 'OU'"
  });
  var AndCriterionForm = CombinedCriterionForm.extend({
    template: "andcriterion_form",
    label: "Configuration d'une clause 'ET'"
  });

  var controller = {
    initialized:false,
    index: function(){
      this.initialize();
      App.popup.empty();
      App.entry_edit.empty();
      this.entry_list_view.fadeIn();
    },
    initialize: function(){
      if (! this.initialized){
        this.sheet_view = new SheetView({model: Statistic.sheet});
        App.sheet.show(this.sheet_view);
        this.entry_list_view = new EntryListView(
          {collection: Statistic.entries}
        );
        App.entries.show(this.entry_list_view);
        this.initialized = true;
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
      var entry_model = Statistic.entries.get(id);
      if (_.isUndefined(entry_model)){
        Statistic.router.navigate('index', {trigger: true});
        return false;
      }
      this.entry_list_view.fadeOut();
      this.current_entry = entry_model;
      this.entry_form = new EntryFormLayout({
        model: entry_model,
        destCollection: Statistic.entries
      });
      App.entry_edit.show(this.entry_form);

      var criteria_root_url = entry_model.criteria_url();

      this.criteria_collection = new CriteriaCollection(
        {url: criteria_root_url, entry_id: entry_model.id }
      );
      var this_ = this;
      return this.criteria_collection.fetch({
        success: function(){
          var criteria_list = new CriteriaListView({
            collection: this_.criteria_collection
          });
          this_.entry_form.getRegion('list').show(criteria_list);
        }
      });
    },
    _buildCriterionForm: function(model){
      var criterionForm;
      var this_ = this;
      if (model.get('type') == 'date'){
        criterionForm = new DateCriterionFormView(
          {model: model, destCollection: this.criteria_collection}
        );
      } else if (model.get('type') == 'multidate'){
        criterionForm = new DateCriterionFormView(
          {model: model, destCollection: this.criteria_collection}
        );
      } else if (model.get('type') == 'string'){
        criterionForm = new StringCriterionView(
          {model: model, destCollection: this.criteria_collection}
        );
      } else if (model.get('type') == 'number'){
        criterionForm = new NumberCriterionView(
          {model: model, destCollection: this.criteria_collection}
        );
      } else if (model.get('type') == 'optrel'){
        criterionForm = new OptRelCriterionForm(
          {
            model: model,
            destCollection: this.criteria_collection}
        );
        criterionForm.optrel_options = AppOptions.optrel_options[model.get('key')];
      } else if (model.get('type') == 'static_opt'){
        criterionForm = new OptRelCriterionForm(
          {
            model: model,
            destCollection: this.criteria_collection}
        );
        criterionForm.optrel_options = AppOptions.static_opt_options[model.get('key')];
      } else if (model.get('type') == 'bool'){
        criterionForm = new BoolCriterionView(
          {model: model, destCollection: this.criteria_collection}
        );
      } else if (model.get('type') == 'or'){
        criterionForm = this.criterionForm = new OrCriterionForm(
          {model: model, destCollection: this.criteria_collection}
        );
      } else if (model.get('type') == 'and'){
        criterionForm = this.criterionForm = new AndCriterionForm(
          {model: model, destCollection: this.criteria_collection}
        );
      }
      this.entry_form.getRegion('form').show(criterionForm);
    },
    criteria_add: function(entry_id, key){
      var this_ = this;
      this.entry_edit(entry_id).then(function(){
        var option = AppOptions.columns[key];

        var model = new CriterionModel({key: key, type:option.type});
        this_._buildCriterionForm(model);
      });
    },
    criteria_edit: function(entry_id, criterion_id){
      var this_ = this;
      this.entry_edit(entry_id).then(function(){
        var model = this_.criteria_collection.get(criterion_id);
        this_._buildCriterionForm(model);
      });
    },
    criteria_or_add: function(entry_id){
      var this_ = this;
      this.entry_edit(entry_id).then(function(){
        var model = new CriterionModel({key: "", type:"or"});
        this_._buildCriterionForm(model);
      });
    },
    criteria_or_edit: function(entry_id, criterion_id){
      var this_ = this;
      this.entry_edit(entry_id).then(function(){
        var model = this_.criteria_collection.get(criterion_id);
        this_._buildCriterionForm(model);
      });
    },
    criteria_and_add: function(entry_id){
      var this_ = this;
      this.entry_edit(entry_id).then(function(){
        var model = new CriterionModel({key: "", type:"and"});
        this_._buildCriterionForm(model);
      });
    },
    criteria_and_edit: function(entry_id, criterion_id){
      var this_ = this;
      this.entry_edit(entry_id).then(function(){
        var model = this_.criteria_collection.get(criterion_id);
        this_._buildCriterionForm(model);
      });
    }
  };
  router = Backbone.Marionette.AppRouter.extend({
    controller: controller,
    appRoutes: {
      "index": "index",
      "entries/:id/edit": "entry_edit",
      "entries/add": "entry_add",
      "entries/:id/orcriteria/add": "criteria_or_add",
      "entries/:id/orcriteria/edit": "criteria_or_edit",
      "entries/:id/andcriteria/add": "criteria_and_add",
      "entries/:id/andcriteria/edit": "criteria_and_edit",
      "entries/:id/criteria/add/:key": "criteria_add",
      "entries/:id/criteria/:cid/edit": "criteria_edit"
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
    var form = form_container.find('form');
    var input = form_container.find('input');
    $('button.btn-add').on('click', function(){
      form_container.fadeIn();
      input.focus();
    });
    form.off('submit');
    form.on("submit", function(event){
      event.preventDefault();
      var title = input.val();
      if (title.length === 0){
        showError(input, "Requis");
      } else {
        hideFormError(form_container);
        var ajax_req = ajax_call( AppOptions['submiturl'], {title: title});
      }
    });
  }
}

$(function(){
  StatisticPageInit();
  StatisticsPageInit();
});
