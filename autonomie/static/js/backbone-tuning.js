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
var ModalRegion = Backbone.Marionette.Region.extend({
  el: "modal",
    constructor: function(){
      Backbone.Marionette.Region.prototype.constructor.apply(this, arguments);
      this.on("show", this.showModal, this);
      setPopUp(this.el, "Title");
    },
    getEl: function(selector){
      var $el = $("#" + selector);
      $el.on("hidden", this.close);
      return $el;
    },
    showModal: function(view){
      view.on("close", this.hideModal, this);
      console.log("Showing the modal");
      this.$el.dialog('open');
    },
    hideModal: function(){
      console.log("Hiding the modal");
      this.$el.dialog('close');
    }
});
