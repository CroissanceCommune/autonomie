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



function showError(control, error){
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
function hideFormError(form){
  /*"""
   * Remove bootstrap style errors from the whole form
   */
    form.find(".alert").remove();
    var groups = form.find(".form-group");
    groups.removeClass("has-error");
    groups.find(".error-message").remove();
    return form;
}
function hideFieldError(control){
  /*"""
   */
   var group = control.parents(".form-group");
   group.removeClass("has-error");
   group.find(".error-message").remove();
   return control;
}
function BootstrapOnValidForm(view, attr, selector){
    var control, group;
    control = view.$('[' + selector + '=' + attr + ']');
    hideFieldError(control);
}
function BootstrapOnInvalidForm(view, attr, error, selector) {
    var control, group, position, target;
    control = view.$('[' + selector + '=' + attr + ']');
    showError(control, error);
}
function setUpBbValidationCallbacks(bb_module){
    _.extend(bb_module, {
        valid: BootstrapOnValidForm,
        invalid: BootstrapOnInvalidForm
    });
}
setUpBbValidationCallbacks(Backbone.Validation.callbacks);
