/*
 * * Copyright (C) 2012-2013 Croissance Commune
 * * Authors:
 *       * Arezki Feth <f.a@majerti.fr>;
 *       * Miotte Julien <j.m@majerti.fr>;
 *       * Pettier Gabriel;
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
