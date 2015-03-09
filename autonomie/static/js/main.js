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


function showLoginDialog(login_form_html){
  /*
   * Popup a login dialog if not already done
   */
  if (!$('#login_form').dialog( "isOpen" )){
    $('#login_form').html(login_form_html);
    $('#login_form').dialog('open');
  }
}

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

function checkLogin(callback){
  /*
   * Check That the current user is logged in
   *
   * :returns:
   * :rtype: bool
   */
  var result = false;
  $.ajax(
    {
      url: '/api/v1/login',
      type: 'GET',
      cache: false,
      dataType: 'json',
      async: false,
      success: function(resp){
        if (resp.status == 'success'){
          if (! _.isUndefined(callback)){
            callback();
          }
          result = true;
        } else {
          showLoginDialog(resp.datas.login_form);
          result = false;
        }
      }
    }
  );
  return result;
}

function ajaxAuthCallback(resp){
  /*
   * call back after the ajax authentication process:
   * Hide the form
   */
  if (resp.status == 'success'){
    $('#login_form').dialog('close');
    $('#login_form').html('');
  }else{
    $('#login_form').html(resp.datas.login_form);
  }
}

function setAuthCheckBeforeSubmit(form){
  /*
   * Check that the user is logged in on form submission
   *
   * :param str form: The form selector string (e.g: "#deform")
   */

  var button = $(form).find('button[type=submit]');

  button.off('click');
  button.click(function(event){
    var resp = checkLogin();
    if (! checkLogin()){
      event.preventDefault();
    }
  });

}


function setPopUp(id, title){
  /*
   * Make the div with id `id` becomes a dialog with title `title`
   */
  $("#" + id).dialog(
      {
        autoOpen: false,
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
          // Fix bootstrap + jqueryui conflict
          var closeBtn = $('.ui-dialog-titlebar-close');
          closeBtn.addClass("ui-button ui-widget ui-state-default " +
            "ui-corner-all ui-button-icon-only");
          closeBtn.html('<span class="ui-button-icon-primary ui-icon ' +
          'ui-icon-closethick"></span><span class="ui-button-text">Close</span>');
            }
        }
    );
  }
  function setClickableRow(){
    /*
     * Set all rows with clickable-row class clickable
     */
    $('.clickable-row').on('click', function(){
      var href = $(this).data("href");
      if (_.isUndefined(href)){
        alert('Erreur, aucun lien spécifié, contactez votre administrateur');
      }else{
        window.document.location = $(this).data("href");
    }
  });
}
$(function(){
  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.nav-tabs a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
  });
  setClickableRow();
  setPopUp('login_form', "Authentification");
});

