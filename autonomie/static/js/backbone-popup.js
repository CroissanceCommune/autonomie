/*
 * File Name : backbone-popup.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

var Popup = Backbone.Marionette.Region.extend({
  /*
   *  Popup object as a marionette region
   *
   *  Avoids problems with zombie views
   */
  el: "#popup",
  constructor:function(){
    _.bindAll(this);
    Backbone.Marionette.Region.prototype.constructor.apply(this, arguments);
  },
  getEl: function(selector){
    var $el = $(selector);
    return $el;
  },
  onShow: function(view){
    /*
     * Popup the element with a custom close function
     */
    var this_ = this;
    view.on("close", this.closeModal, this);
    this.$el.dialog({
        resize:'auto',
        modal:true,
        width:"auto",
        height:"auto",
        title:this_.title,
        hide: "fadeOut",
        close:function(event, ui){
          this_.close();
        }
    });
  },
  closeModal: function(){
    if (this.$el.dialog("isOpen")){
      this.$el.dialog("close");
    }
  }
});
