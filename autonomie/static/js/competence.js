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
  items: '#itemslist'
});

AutonomieApp.module('Competence', function(Competence, App, Backbone, Marionette, $, _){
  Competence.on('start', function(){
    console.log("Starting the competence module");
  });
});

function CompetencePageInit(options){
  if (AppOptions['loadurl'] !== undefined){
    // page statistic
    var module = AutonomieApp.module('Competence');
    // Quand on start on lance initModule en callback de la requête jquery
    var options_load = initLoad(AppOptions['loadurl']).then(
      function(data){
        console.log("Options loaded");
        _.extend(AppOptions, data);
      }
    );
    var grid_load = initLoad(AppOptions['contexturl']);
    grid_load.then(function(datas){
      console.log("datas loaded");
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
