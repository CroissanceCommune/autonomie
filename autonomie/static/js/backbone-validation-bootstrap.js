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
_.extend(Backbone.Validation.callbacks, {
  valid: function(view, attr, selector) {
    var control, group;
    control = view.$('[' + selector + '=' + attr + ']');
    group = control.parents(".control-group");
    group.removeClass("error");
     return group.find(".help-inline.error-message").remove();
  },
  invalid: function(view, attr, error, selector) {
    var control, group, position, target;
    control = view.$('[' + selector + '=' + attr + ']');
    group = control.parents(".control-group");
    group.addClass("error");
    if (group.find(".help-inline").length === 0) {
      group.find(".controls").append("<span class=\"help-inline error-message\"></span>");
    }
    target = group.find(".help-inline");
    return target.text(error);
  }
});
