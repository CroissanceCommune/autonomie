/*
 * File Name :
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 * Adapted the original : https://gist.github.com/2909552
 *
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
   return form;
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
