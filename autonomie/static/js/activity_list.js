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
var ActivityModule = AutonomieApp.module('ActivityModule' ,
  function (ActivityModule, AutonomieApp, Backbone, Marionette, $, _){
    ActivityModule.startWithParent = false;
    ActivityModule.Router = Marionette.AppRouter.extend({
      appRoutes: {
        "activities/:id": "get_activities"
        }
    });
    ActivityModule.Controller = {
      initialized: false,
      element: '#activitylist_container',

      initialize: function(){
        if (!this.initialized){
          this.$element = $(this.element);
          this.initialized = true;
          _.bindAll(this, 'displayList');
        }
      },
      setNbItemsSelectBehaviour: function(){
        $('#number_of_activities').unbind('change.activities');
        _.bindAll(this, 'get_activities');
        var this_ = this;
        $('#number_of_activities').bind("change.activities",
          function(){
            this_.get_activities(1);
          }
        );
      },
      index: function(){
        this.initialize();
        this.setNbItemsSelectBehaviour();
      },
      get_activities: function(id){
        this.initialize();
        this.refresh_list(id);
      },
      refresh_list: function(page_num) {
        url = '?action=activities_html';
        var items_per_page = $('#number_of_activities').val();
        postdata = {'activities_page_nb': page_num,
                    'activities_per_page': items_per_page};
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
      // We manually launch the index since it's not the role of our activity
      // module to do that
      ActivityModule.router = new ActivityModule.Router( {controller: ActivityModule.Controller});
      ActivityModule.Controller.index();
    });
    }
);


$(function(){
  AutonomieApp.start();
  AutonomieApp.module('ActivityModule').start();
});

