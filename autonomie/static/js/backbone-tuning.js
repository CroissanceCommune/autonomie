/*
 * File Name : backbone-tuning.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
// Override backbone marionette's render method to fit hogan templating
Backbone.Marionette.Renderer.render = function(template_obj, data){
  return template_obj.render(data);
};
