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
