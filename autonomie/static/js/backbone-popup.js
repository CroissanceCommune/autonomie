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



var Popup = Backbone.Marionette.Region.extend({
  /*
   *  Popup object as a marionette region
   *
   *  Avoids problems with zombie views
   */
  el: "#popup",
  constructor:function(){
    _.bindAll(this, "closeModal", "reset", "onShow", "getEl");
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
    var window_height = $(window).height();
    var window_width = $(window).width();
    var this_ = this;
    view.on("close", this.closeModal, this);
    this.$el.dialog({
      autoOpen: false,
      height:"auto",
      width: "auto",
      resizable: false,
      modal:true,
      fluid: true,
      position: ['center','middle'],
      maxHeight: window_height * 0.9,
      maxWidth: window_width * 0.9,
      title:this_.title,
      hide: "fadeOut",
      open: function(event, ui){
        //$(this).css('height','auto');
        // Get the content width
        var content_width = $(this).children().first().width();
        var window_ratio = window_width * 0.8;

        // Get the best width to use between window's or content's
        var dialog_width = Math.min(content_width + 50, window_ratio);
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
      },
      close:function(event, ui){
        this_.close();
      }
    });
    this.$el.dialog('open');
  },
  closeModal: function(){
    if (this.$el.dialog("isOpen")){
      this.$el.dialog("close");
    }
  }
});
