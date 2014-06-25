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
    ActivityModule.Router = Marionette.AppRouter.extend({
      appRoutes: {
        "events/:id": "get_events"
        }
    });
    ActivityModule.Controller = {
      initialized: false,
      element: '#event_container',

      initialize: function(){
        if (!this.initialized){
          this.$element = $(this.element);
          this.initialized = true;
          _.bindAll(this, 'displayList');
        }
      },
      setNbItemsSelectBehaviour: function(){
        $('#number_of_events').unbind('change.events');
        _.bindAll(this, 'get_events');
        var this_ = this;
        $('#number_of_events').bind("change.events",
          function(){
            this_.get_events(1);
          }
        );
      },
      index: function(){
        this.initialize();
        this.setNbItemsSelectBehaviour();
      },
      get_events: function(id){
        this.initialize();
        this.refresh_list(id);
      },
      refresh_list: function(page_num) {
        url = '?action=events_html';
        var items_per_page = $('#number_of_events').val();
        postdata = {'events_page_nb': page_num,
                    'events_per_page': items_per_page};
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
      // We manually launch the index since it's not the role of our event
      // module to do that
      console.log("Start The Activity Module");
      ActivityModule.router = new ActivityModule.Router( {controller: ActivityModule.Controller});
      ActivityModule.Controller.index();
    });
    }
);

