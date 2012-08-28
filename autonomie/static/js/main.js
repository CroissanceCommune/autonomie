/*
 * File Name : main.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
function setPopUp(id, title){
  /*
   * Make the div with id `id` becomes a dialog with title `title`
   */
  $("#" + id).dialog(
    { autoOpen: false,
      modal:true,
      width:"auto",
      title:title,
      open: function(event, ui){
        $('.ui-widget-overlay').css('width','100%');
        $('.ui-widget-overlay').css('height','100%');
      }
    });
}
