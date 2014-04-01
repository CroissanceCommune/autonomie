/*
 * * Copyright (C) 2012-2013 Croissance Commune
 * * Authors:
 *       * Arezki Feth <f.a@majerti.fr>;
 *       * Miotte Julien <j.m@majerti.fr>;
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

var TaskModule = AutonomieApp.module('TaskModule' ,
  function (TaskModule, AutonomieApp, Backbone, Marionette, $, _){
    TaskModule.startWithParent = false;
    TaskModule.Router = Marionette.AppRouter.extend({
      appRoutes: {
        "tasklist/:id": "get_tasks"
        }
    });
    TaskModule.Controller = {
      initialized: false,
      element: '#tasklist_container',

      initialize: function(){
        if (!this.initialized){
          this.$element = $(this.element);
          this.initialized = true;
          _.bindAll(this, 'displayList');
        }
      },
      setNbItemsSelectBehaviour: function(){
        $('#number_of_tasks').unbind('change.tasks');
        _.bindAll(this, 'get_tasks');
        var this_ = this;
        $('#number_of_tasks').bind("change.tasks",
          function(){
            this_.get_tasks(1);
          }
        );
      },
      index: function(){
        this.initialize();
        this.setNbItemsSelectBehaviour();
      },
      get_tasks: function(id){
        this.initialize();
        this.refresh_list(id);
      },
      refresh_list: function(page_num) {
        url = '?action=tasks_html';
        var items_per_page = $('#number_of_tasks').val();
        postdata = {'tasks_page_nb': page_num,
                    'tasks_per_page': items_per_page};
        var this_ = this;
        $.ajax(
            url,
            {
              type: 'POST',
              data: postdata,
              dataType: 'html',
              success: function(data){
                this_.displayList(data);
              },
              error: function(){
                displayServerError("Une erreur a été rencontrée lors de " +
                "la récupération des dernières activités");
              }
            }
            );
      },
      displayList: function(data){
        this.$element.html(data);
        this.setNbItemsSelectBehaviour();
      }
    };
    AutonomieApp.addInitializer(function(){
      // Here we have code launched before backbone history starts (we need to
      // create all routers before))
      // We manually launch the index since it's not the role of our task
      // module to do that
      TaskModule.router = new TaskModule.Router( {controller: TaskModule.Controller});
      TaskModule.Controller.index();
    });
    }
);


$(function(){
  AutonomieApp.start();
  AutonomieApp.module('TaskModule').start();
});
