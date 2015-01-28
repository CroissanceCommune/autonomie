/*
 * File Name : job.js
 *
 * Copyright (C) 2014 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
/*
 * Job view js code (model and view)
 */
var AppOptions = {};
var JobModule = AutonomieApp.module(
  "JobModule",
  function(JobModule, AutonomieApp, Backbone, Marionette, $, _){
    var JobView = Marionette.ItemView.extend({
      tagName: "div",
      initialize: function(datas){
        this.listenTo(this.model, 'change', this.render, this);
        this.dataType = datas['dataType'];
      },
      getTemplate: function(){
        // Le nom du template correspond au type_ du modèle de job que l'on
        // affiche
        return this.dataType;
      },
      templateHelpers: function(){
        var failed = false;
        var running = true;
        if (this.model.get('status') == 'failed'){
          failed = true;
          running = false;
        }else{
          if (this.model.get('status') == 'completed'){
            running = false;
          }
        }
        var has_err_message = false;
        var err_message = "";
        _.each(this.model.get('error_messages'), function(item){
            if (item !== ''){
              err_message += item + "<br />";
              has_err_message = true;
            }
          }
        );
        var has_message = false;
        var message = "";
        _.each(this.model.get('messages'), function(item){
            if (item !== ''){
              message += item + "<br />";
              has_message = true;
            }
          }
        );

        return {
          running: running,
          failed: failed,
          err_message: new Handlebars.SafeString(err_message),
          message: new Handlebars.SafeString(message),
          has_message: has_message,
          has_err_message: has_err_message,
          dataType: this.dataType
          };
      }
    });
    var JobModel = Backbone.Model.extend({
      initialize: function(args){
        this.url = args.url;
        var reload = _.bind(this.reload, this);
        this.scheduler = setInterval(reload, 1000);
      },
      reload: function(){
        if ((this.get('status') == 'completed') || (this.get('status') == 'failed')){
          clearInterval(this.scheduler);
        }
        this.fetch();
      }
    });
    JobModule.addInitializer(function(options){
      JobModule.job = new JobModel({url: AppOptions.url});
      JobModule.job_view = new JobView(
          {model: JobModule.job, dataType: AppOptions.dataType}
        );
      AutonomieApp.job.show(JobModule.job_view);
    });
  }
);
AutonomieApp.addRegions({
  job: "#ajax_container"
});
