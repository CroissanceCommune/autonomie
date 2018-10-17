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


function setPopUp(element, title){
  /*
   * Make the div with element `element` becomes a dialog with title `title`
   */
  var isjquery = element instanceof jQuery;
  if (! isjquery){
    if (_.indexOf(element, '#') !== 0){
      element = '#' + element;
    }
    element = $(element);
  }
  var window_height = $(window).height();
  var window_width = $(window).width();
  $(element).dialog({
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
        console.log("The dialog content width is %s", content_width);
        var window_width = $(window).width();
        var window_ratio = window_width * 0.8;

        // Get the best width to use between window's or content's
        var dialog_width = Math.min(content_width + 50, window_width);
        var dialog = $(this).parent();
        dialog.width(dialog_width);

        // We need to set the left attr
        var padding = (window_width - dialog_width) / 2.0;
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
function highlight_error(jquery_tag, callback){
  /*
   * Display a main error message and highlight a jquery tag in red
   * Optionnaly launch a callback
   */
  displayServerError("Une erreur a été rencontrée lors de la " +
    "sauvegarde de vos données");
  return highlight(jquery_tag, "#F9AAAA", callback);
}
function highlight_success(jquery_tag, callback){
  /*
   * Display a main success message and highlight a jquery tag in green
   * Optionnaly launch a callback
   */
  displayServerSuccess("Vos données ont bien été sauvegardées");
  return highlight(jquery_tag, "#ceff99", callback);
}
function highlight(jquery_tag, color, callback){
  color = color || "#ceff99";
  jquery_tag.css("backgroundColor", "#fff");
  return jquery_tag.effect('highlight', {color: color}, 1500,
    function(){if (callback !== undefined){ callback();} }
  );
}

function ajax_request(url, data, method, extra_options){
  /*
   * Returns a deferred ajax request
   *
   * :param url: the url
   * :param data: the datas to send as an object
   * :param options: an object with other jquery ajax options
   *
   *   ex:
   *    var ajax_call = ajax_request(url, {mesdonnées});
   *    ajax_call.then(function(response){
   *      custom code
   *    });
   */
   var data = data || {};
   var method = method || 'POST';
    var options = {
        url: url,
        data: data,
        method: method,
        dataType: 'json',
        cache: false
    }
    if ((method == 'POST') || (method=='PUT') || (method='PASTE')){
        options.data = JSON.stringify(data);
        options.contentType = "application/json; charset=UTF-8";
        options.processData = false;
    }

    _.extend(options, extra_options);

    return $.ajax(options);
}
var ajax_call = ajax_request;
function loadUI(ui_object){
  /*
   * loadUI elements : the UI object is global and is used as a cache
   * on page load, it replaces string selectors by jquery object avoiding to
   * access too many times the DOM
   *
   * :param object ui_object: a js object with key value pairs :
   *    * value: a jquery selector (ex : #id-de-ma-div)
   *
   *
   * If you want to use this : create a js object (can be global)
   * var UI = {select_nom: "#select-nom"}
   *
   * This way :
   *  * you can have a jquery objects cache
   *  * you can easily retrieve your objects selectors on a single place in
   *  your js file
   */
  // Pour chaque clé dans l'objet UI on remplace la valeur par l'objet jquery
  // correspondant
  var key;
  for (key in ui_object){
    var selector = ui_object[key];
    if (!_.isString(selector)){
      // On a un objet jquery (on reload) qui peut avoir été récupéré avant un
      // rafraichissement du DOM, on ne veut donc pas cet élément de DOM là,
      // mais son clone que l'on récupère en utilisant le même selector
      selector = selector.selector;
    }
    ui_object[key] = $(selector);
  }
}

function showLoader(){
  /*
   * Shows a loader in the given tag
   */
  $('#loading-box').show();
}


// Important point : handle redirection by json dict for ajax calls
// Expects a redirect value to be returned with the 302 code
function setupJsonRedirect() {
  $(document).ajaxComplete(
    function( event, xhr, settings ) {
        var json_resp;
        if (! _.isUndefined(xhr.responseJSON)){
            json_resp = xhr.responseJSON;
        } else {
            json_resp = $.parseJSON(xhr.responseText);
        }

        if (!_.isUndefined(json_resp) && ( json_resp.redirect )){
            window.location.href = json_resp.redirect;
        }
    }
  );
}

function cleanTinyMceEditors(){
  var editors = [];
  for (var i=0; i < tinyMCE.editors.length; i++){
    var editor = tinyMCE.editors[i];
    if ($("#" + editor.id).length === 0){
      try{
        i = i-1;
        delete tinyMCE.remove(editor);
      } catch (e){}
    }
  }
  tinyMCE.triggerSave();
}

function setupTinyMceHack(){
  if (typeof(tinyMCE) != 'undefined'){
    $('form').on('submit.hack', function(event){
      cleanTinyMceEditors(event, this);
    });
  }
}

function setupMainBehaviours(){
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
  setupJsonRedirect();
  setupTinyMceHack();
  $.ui.dialog.prototype._allowInteraction = function(e) {
        return !!$(e.target).closest('.ui-dialog, .ui-datepicker, .select2-drop').length;
  };
}

window.openPopup = function(url){
    var screen_width =  screen.width;
    var screen_height = screen.height;
    var width = getPercent(screen_width, 60);
    var height = getPercent(screen_height, 60);
    var uniq_id = _.uniqueId('popup');
    if (_.indexOf(url, '?') != -1){
        url = url + "&popup=" + uniq_id;
    } else {
        url = url + "?popup=" + uniq_id;
    }

    var new_win = window.open(url, uniq_id, "width=" + width + ",height=" + height);
    return false;
}

window.dismissPopup = function(win, options){
    var default_options = {refresh: true};
    _.extend(default_options, options);
    win.close();
    if (!_.isUndefined(default_options.force_reload)){
        window.location.reload();
    } else {
        var new_content = "";

        if (!_.isUndefined(default_options.message)){
            new_content += "<div class='alert alert-success text-center'>";
            new_content += default_options.message;
        } else if (!_.isUndefined(default_options.error)){
            new_content += "<div class='alert alert-danger text-center'>";
            new_content += default_options.error;
        }

        if (default_options.refresh){
            new_content += "&nbsp;<a href='#' onclick='window.location.reload();'><i class='glyphicon glyphicon-refresh'></i> Rafraîchir</a>";
        }

        new_content += '</div>';
        var dest_tag = $('#popupmessage');
        if (dest_tag.length == 0){
            dest_tag = $('.pagetitle');
        }
        dest_tag.after(new_content);
    }
}

$(setupMainBehaviours);
function capitalize(string){
    return string.charAt(0).toUpperCase() + string.substring(1).toLowerCase();
}
