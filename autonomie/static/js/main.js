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
// Important point : handle redirection by json dict for ajax calls
// Expects a redirect value to be returned with the 302 code
$(document).ready(
    function() {
      $('body').ajaxComplete(
        function( data, xhr, settings ) {
          json_resp = jQuery.parseJSON( xhr.responseText );
          if ( json_resp.redirect ){
            window.location.href = json_resp.redirect;
          }
        }
      );
    }
);
function setPopUp(id, title){
  /*
   * Make the div with id `id` becomes a dialog with title `title`
   */
  $("#" + id).dialog(
      { autoOpen: false,
        resize:'auto',
    modal:true,
    width:"auto",
    height:"auto",
    title:title,
    open: function(event, ui){
      $('.ui-widget').css('width','60%');
      $('.ui-widget').css('height','80%');
      $('.ui-widget').css('left', '20%');
      $('.ui-widget-content').css('height','auto');
    }
      });
}
