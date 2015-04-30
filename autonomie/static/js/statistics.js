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

AutonomieApp.addInitializer(function(options){
  if (AppOptions['loadurl'] !== undefined){
    $.ajax({
      url: AppOptions['loadurl'],
      dataType: 'json',
      async: false,
      mimeType: "textPlain",
      data: {},
      cache: false,
      success: function(data) {
        _.extend(AppOptions, data['options']);
      },
      error: function(){
        alert("Une erreur a été rencontrée, contactez votre administrateur.");
      }
    });
  } else {
    alert("Une erreur a été rencontrée, contactez votre administrateur.");
  }
});
