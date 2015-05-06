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
var AppOptions = {};

AutonomieApp.addRegions({
  sheet: "#sheet",
  entries: '#entrylist'
});


AutonomieApp.module('Statistic', function(Statistic, App, Backbone, Marionette, $, _){
  // On lance le module si besoin depuis le code un peu plus bas
  this.startWithParent = false;

  var SheetModel = Backbone.Model.extend({
    root_url: "/statistics",
    validation:{
      title: {
        required:true,
        msg:"est requis"
      }
    },
    url: function(){
      return this.root_url + "/" + this.id + "?action=edit";
    }
  });
  var EntryModel = Backbone.Model.extend({});
  var EntryCollection = Backbone.Collection.extend({
    model: EntryModel
  });
  var EntryView = Marionette.ItemView.extend({
    template: "entry",
    tagName: "tr"
  });
  var EntryListView = Marionette.CompositeView.extend({
    childView: EntryView,
    template: "entry_list",
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
    initialize: function(args){
      // Bind to change event
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
    },
    initialize: function(){
      if (! this.initialized){
        this.sheet_view = new SheetView({model: Statistic.sheet});
        App.sheet.show(this.sheet_view);
        console.log(Statistic.entries);
        this.entry_list_view = new EntryListView(
          {collection: Statistic.entries}
        );
        App.entries.show(this.entry_list_view);
      }
    }

  };
  router = Backbone.Marionette.AppRouter.extend({
    controller: controller,
    appRoutes: {
      "index": "index"
    }
  });
  Statistic.initModule = function(){
    var data = Statistic.datas;
    Statistic.router = new router();
    Statistic.sheet = new SheetModel(data['sheet']);
    console.log(data['entries']);
    Statistic.entries = new EntryCollection(data['entries']);
    console.log(Statistic.entries);
    Statistic.router.controller.index();

  };
});



function StatisticPageInit(options){
  if (AppOptions['loadurl'] !== undefined){
    // page statistic
    var module = AutonomieApp.module('Statistic');
    // Quand on start on lance initModule en callback de la requête jquery
    module.on('start', module.initModule);

    var options_load = initLoad(AppOptions['loadurl']).then(
      function(data){
        _.extend(AppOptions, data['options']);
      }
    );
    var sheet_load = initLoad(AppOptions['contexturl']);
    sheet_load.then(function(datas){
      module.datas = datas;
    });
    $.when(options_load, sheet_load).then(
      function(datas){
        module.start();
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

AutonomieApp.addInitializer(StatisticPageInit);
AutonomieApp.addInitializer(StatisticsPageInit);
