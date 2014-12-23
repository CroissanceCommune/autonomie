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
      initialize: function(){
        this.listenTo(this.model, 'change', this.render, this);
      },
      getTemplate: function(){
        return "csv_import_job";
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
        return {
          running: running,
          failed: failed
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
      JobModule.job_view = new JobView({model: JobModule.job});
      AutonomieApp.job.show(JobModule.job_view);
    });
  }
);
AutonomieApp.addRegions({
  job: "#ajax_container"
});
