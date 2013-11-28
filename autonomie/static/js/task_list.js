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

var MyApp = new Backbone.Marionette.Application();

MyApp.on("initialize:after", function(){
  /*
   *""" Launche the history (controller and router stuff)
   */
  console.log("Launching backbone's history'");
  if ((Backbone.history)&&(! Backbone.History.started)){
    Backbone.history.start();
  }
});

MyApp.Router = Backbone.Marionette.AppRouter.extend({
  appRoutes: {
    "": "index",
    "index": "index",
    "tasklist/:id": "get_tasks"
  }
});

MyApp.Controller = {
  initialized: false,
  element: '#tasklist_container',

  initialize: function(){
    console.log("Initialize");
    if (!this.initialized){
      this.$element = $(this.element);
      this.initialized = true;
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
    console.log("Coming on the index page");
    this.initialize();
    this.setNbItemsSelectBehaviour();
  },
  get_tasks: function(id){
    console.log("Getting tasks");
    this.initialize();
    this.refresh_list(id);
  },
  refresh_list: function(page_num) {
    console.log("Recuperation en cours: page " + page_num);
    url = '?action=tasks_html';
    var items_per_page = $('#number_of_tasks').val();
    postdata = {'tasks_page_nb': page_num,
                'tasks_per_page': items_per_page};
    var this_ = this;
    $.post(
        url,
        postdata,
        function(data, httpstatus, xhr){
            /* TODO: handle failure.
             * I got in trouble with callbacks */
            this_.$element.html(data);
            this_.setNbItemsSelectBehaviour();
        },
        'text');
  },
}

MyApp.addInitializer(function(options){
  /*
   *  Application initialization
   */
  MyApp.router = new MyApp.Router({controller:MyApp.Controller});
});

$(function(){
  console.log("Starting my application");
  MyApp.start();
});
