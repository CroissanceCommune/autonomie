/*
 * * Copyright (C) 2012-2017 Croissance Commune
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

const showError = function(control, error){
  /*"""
   * shows error 'message' to the group group in a twitter bootstrap
   * friendly manner
   */
  var group = control.parents(".form-group");
  group.addClass("has-error");
  if (group.find(".help-block").length === 0){
    group.append(
    "<span class=\"help-block error-message\"></span>");
  }
  var target = group.find(".help-block");
  return target.text(error);
}
const hideFormError = function(form){
  /*"""
   * Remove bootstrap style errors from the whole form
   */
    form.find(".alert").remove();
    var groups = form.find(".form-group");
    groups.removeClass("has-error");
    groups.find(".error-message").remove();
    return form;
}
const hideFieldError = function(control){
  /*"""
   */
   var group = control.parents(".form-group");
   group.removeClass("has-error");
   group.find(".error-message").remove();
   return control;
}
export const BootstrapOnValidForm = function(view, attr, selector){
    var control, group;
    control = view.$('[' + selector + '=' + attr + ']');
    hideFieldError(control);
}
export const BootstrapOnInvalidForm = function(view, attr, error, selector) {
    var control, group, position, target;
    control = view.$('[' + selector + '=' + attr + ']');
    showError(control, error);
}
export const setUpBbValidationCallbacks = function(bb_module){
    _.extend(bb_module, {
        valid: BootstrapOnValidForm,
        invalid: BootstrapOnInvalidForm
    });
}
const _displayServerMessage = function(options){
  /*
   * """ Display a message from the server
   */
//   var msgdiv = require('../handlebars/serverMessage.mustache');
//   $(msgdiv).prependTo("#messageboxes").fadeIn('slow').delay(8000).fadeOut(
//   'fast', function() { $(this).remove(); });
   console.log(options);
}
export const displayServerError = function(msg){
  /*
   *  Show errors in a message box
   */
  _displayServerMessage({msg:msg, error:true});
}
export const displayServerSuccess = function(msg){
  /*
   *  Show errors in a message box
   */
  _displayServerMessage({msg:msg});
}
