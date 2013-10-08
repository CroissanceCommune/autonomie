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
  var group = control.parents(".control-group");
  group.addClass("error");
  if (group.find(".help-inline").length === 0){
    group.find(".controls").append(
    "<span class=\"help-inline error-message\"></span>");
  }
  var target = group.find(".help-inline");
  return target.text(error);
}
function hideFormError(form){
  /*"""
   * Remove bootstrap style errors from the whole form
   */
    form.find(".alert").remove();
    var groups = form.find(".control-group");
    groups.removeClass("error");
    groups.find(".help-inline.error-message").remove();
    groups.find(".help-inline .error").remove();
    return form;
}
function hideFieldError(control){
  /*"""
   */
   var group = control.parents(".control-group");
   group.removeClass("error");
   group.find(".help-inline.error-message").remove();
   return control;
}
_.extend(Backbone.Validation.callbacks, {
  valid: function(view, attr, selector) {
    var control, group;
    control = view.$('[' + selector + '=' + attr + ']');
    hideFieldError(control);
  },
  invalid: function(view, attr, error, selector) {
    var control, group, position, target;
    control = view.$('[' + selector + '=' + attr + ']');
    showError(control, error);
  }
});
