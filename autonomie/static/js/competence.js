/*
 * File Name : competence.js
 *
 * Copyright (C) 2015 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
var AppOptions = {};

AutonomieApp.addRegions({
  items: '#itemslist',
  container: '#itemcontainer'
});

AutonomieApp.module('Competence', function(Competence, App, Backbone, Marionette, $, _){
  var ItemModel = Backbone.Model.extend({
    defaults: {
      active_link: false
    },
    setActive: function(){
      this.set('active_link', true);
    },
    setUnactive: function(){
      this.set('active_link', false);
    },
    subitems_url: function(){
      return this.url() + "/subitems";
    }
  });

  var ItemCollection = Backbone.Collection.extend({
    model: ItemModel,
    setUnactive: function(){
      console.log("Set unactive");
      _.each(this.models, function(model){
        model.setUnactive();
      });
    }  });
  var SubItemModel = Backbone.Model.extend({});
  var SubItemCollection = Backbone.Collection.extend({
    model: SubItemModel
  });

  var ItemView = Marionette.ItemView.extend({
    template: "item",
    tagName: "li",
    className: "",
    modelEvents: {
      "change:active_link": "setActive"
    },
    setActive: function(){
      if (this.model.get('active_link')){
        this.$el.addClass('active');
      } else {
        this.$el.removeClass('active');
      }
    }
  });

  var ItemListView = Marionette.CompositeView.extend({
    childView: ItemView,
    template: "item_list",
    childViewContainer: "ul"
  });

  var SubItemView = BaseTableLineView.extend({
    template: "subitem",
    tagName: "tr",
    className: "",
    events: {
      "change input[type=radio]": "toggleScale"
    },
    toggleScale: function(event){
      var tag = $(event.target);
      var row = this.$el.find('td');
      this.model.set('evaluation', tag.val());
      this.model.save(null, {
        success: function(){
          highlight_success(row);
        },
        error: function(){
          highlight_error(row);
        },
        wait: true
      });
    },
    getScales: function(){
      var evaluation = this.model.get('evaluation');
      // On récupère les éléménts dans l'ordre
      var scales = _.sortBy(AppOptions.scales, 'value');
      // On ajoute le champ par défaut et on récupère le dernier scale pour
      // lequel l'évaluation est supérieur ou égal
      var evaluated;
      _.each(
        scales,
        function(elem){
          elem.is_selected = false;
          if ((evaluation >=0) && (evaluation >= elem.value)){
            evaluated = elem;
          }
        }
      );
      if (!_.isUndefined(evaluated)){
        evaluated.is_selected = true;
      }

      return scales;
    },
    templateHelpers: function(){
      return {"scales": this.getScales()};
    }
  });

  var ItemFormView = Marionette.CompositeView.extend({
    childView: SubItemView,
    template: "item_form",
    childViewContainer: "tbody",
    events: {
      "blur textarea": "onTextAreaBlur"
    },
    ui:{
      textareas: "textarea"
    },
    collectionEvents: {
      "change": "render"
    },
    getScales: function(){
      var requirement = this.model.get('requirement');
      // On récupère les éléménts dans l'ordre
      var scales = _.sortBy(AppOptions.scales, 'value');
      // On ajoute le champ par défaut et on récupère le dernier scale pour
      // lequel le requirement est supérieur ou égal
      var required = scales[0];
      _.each(
        scales,
        function(elem){
          elem.is_reference = false;
          if (requirement >= elem.value){
            required = elem;
          }
        }
      );
      required.is_reference = true;
      return scales;
    },
    getDatasObject: function(jquery_tag){
      var datas = {};
      var val = $.trim(jquery_tag.val());
      var name = jquery_tag.attr('name');
      var prec_val = $.trim(this.model.get(name));
      if (val != prec_val){
        datas[name] = val;
      }
      return datas;
    },
    onTextAreaBlur: function(event){
      var jquery_tag = $(event.target);
      var datas = this.getDatasObject(jquery_tag);
      this.save(datas, jquery_tag);
    },
    save: function(datas, jquery_tag){
      if (!_.isEmpty(datas)){
        var this_ = this;
        _.each(datas, function(val, name){
          this_.model.set(name, val);
        });
        this.model.save(
          datas,
          {
            success: function(){
              highlight_success(jquery_tag);
            },
            error: function(){
              highlight_error(jquery_tag);
            },
            wait: true
          }
        );
      }
    },
    getAverageLevel: function(){
      var value = 0.0;
      _.each(this.collection.models, function(item){
        var val = item.get('evaluation');
        if (!_.isNull(val)){
          value += val;
        }
      });
      return value / this.collection.models.length;
    },
    templateHelpers: function(){
      var average_level = this.getAverageLevel();
      var is_ok_average = average_level >= this.model.get('requirement');
      return {
        average_level: average_level,
        is_ok_average: is_ok_average,
        scales: this.getScales(),
        deadline_label: Competence.datas.grid.deadline_label
      };
    }
  });

  var controller = {
    initialized:false,
    index: function(){
      this.initialize();
    },
    initialize: function(){
      if (! this.initialized){
        this.item_list_view = new ItemListView(
          {collection: Competence.items}
        );
        App.items.show(this.item_list_view);
      }
    },
    item_edit: function(id){
      this.initialize();
      var item_model = Competence.items.get(id);
      Competence.items.setUnactive();
      item_model.setActive();
      if (_.isUndefined(item_model)){
        Competence.router.navigate('index', {trigger: true});
        return false;
      }
      this.current_item = item_model;
      var subitems_url = item_model.subitems_url();
      console.log("url : %s", subitems_url);
      this.subitems = new SubItemCollection();
      this.subitems.url = item_model.subitems_url();
      var this_ = this;
      this.subitems.fetch({
        success: function(){
          this_.item_form = new ItemFormView({
            model: item_model,
            collection: this_.subitems
          });
          App.container.show(this_.item_form);
        }
      });
      return true;
    }
  };
  var router = Backbone.Marionette.AppRouter.extend({
    controller: controller,
    appRoutes: {
      "index": "index",
      "items/:id/edit": "item_edit"
    }
  });
  Competence.on('start', function(){
    var datas = Competence.datas;
    Competence.router = new router();
    Competence.items = new ItemCollection(datas['items']);
    Competence.items.url = AppOptions['item_root_url'];
    Competence.router.controller.index();
  });
});

function CompetencePageInit(options){
  if (AppOptions['loadurl'] !== undefined){
    // page statistic
    var module = AutonomieApp.module('Competence');
    // Quand on start on lance initModule en callback de la requête jquery
    var options_load = initLoad(AppOptions['loadurl']).then(
      function(data){
        _.extend(AppOptions, data);
      }
    );
    var grid_load = initLoad(AppOptions['contexturl']);
    grid_load.then(function(datas){
      module.datas = datas;
    });
    $.when(options_load, grid_load).then(
      function(datas){
        AutonomieApp.start();
      }
    );
  }
}

$(function(){
  CompetencePageInit();
});
