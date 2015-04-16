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
  var window_height = $(window).height();
  var window_width = $(window).width();
  $("#" + id).dialog({
      autoOpen: false,
      height:"auto",
      width: "auto",
      resizable: true,
      modal:true,
      fluid: true,
      position: ['center','middle'],
      maxHeight: window_height * 0.9,
      maxWidth: window_width * 0.9,
      title: title,
      hide: "fadeOut",
      open: function(event, ui){
        //$(this).css('height','auto');
        // Get the content width
        var content_width = $(this).width();
        var window_width = $(window).width();
        var window_ratio = window_width * 0.8;

        // Get the best width to use between window's or content's
        var dialog_width = Math.min(content_width + 50, window_width);
        var dialog = $(this).parent();
        dialog.width(dialog_width);

        // We need to set the left attr
        var padding = (window_width - dialog_width) / 2.0;
        console.log("Setting the padding to %spx", padding);
        dialog.css('left', padding + 'px');

        // Fix dialog height if content is too big for the current window
        if (dialog.height() > $(window).height()) {
            dialog.height($(window).height()*0.9);
        }
        // Show close button (jquery + bootstrap problem)
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
function enableForm(form_id){
  $(form_id).find('select').prop('disabled', false);
  $(form_id).find('input').prop('disabled', false);
  $(form_id).find('select').select2('enable', true);
  $(form_id).find('textarea').prop('disabled', false);
  $(form_id).find('button[type=submit]').prop('disabled', false);
  $(form_id).find('a').removeClass('disabled');
}
function disableForm(form_id){
  $(form_id).find('select').prop('disabled', true);
  $(form_id).find('input').prop('disabled', true);
  $(form_id).find('select').select2('enable', false);
  $(form_id).find('textarea').prop('disabled', true);
  $(form_id).find('button[type=submit]').prop('disabled', true);
  $(form_id).find('a').addClass('disabled');
}
function submitForm(form_selector, name){
  /*
   * Submit a form from outside
   *
   * :param str name: The name of the button we want to click on
   *  (see bugs.jquery.com/ticket/4652 to understand why we don't use simply
   *  form.submit())
   */
  var btn_name = name || 'submit';
  var form_object = $(form_selector);

  var btn_object = form_object.find("button[name=" + btn_name + "]");
  if (btn_object.length === 0){
    console.log("No form submit button match this name : %s", btn_name );
    if (btn_name === 'submit'){
      form_object.submit();
    }
  }else{
    btn_object.click();
  }
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

