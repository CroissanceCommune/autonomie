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


// Override backbone marionette's render method to fit hogan templating
Backbone.Marionette.Renderer.render = function(template_obj, data){
  return template_obj.render(data);
};


var Autonomie = {};


// Provide a default table item view
var BaseTableLineView = Backbone.Marionette.ItemView.extend({
  highlight: function( callback ){
    /*
     * Ok highlight
     */
    this._highlight("#ceff99", callback);
  },
  error: function(callback){
    /*
     * Error highlight
     */
    this._highlight("#F9AAAA", callback);
  },
  _highlight: function(color, callback){
    /*
     * scroll to the view, highlight with the given color and launch the
     * callback
     */
    var top = this.$el.offset().top - 50;
    $('html, body').animate({scrollTop: top});
    // Silly hack to provide highlights on webkit browsers
    this.$el.css("backgroundColor", "#fff");
    this.$el.effect('highlight', {color:color}, 1500,
                    function(){if (callback !== undefined){ callback();}
                });
  }
});
var BaseFormView = Backbone.Marionette.CompositeView.extend({
  events: {
    'click button[name=submit]':'submit',
    'click button[name=cancel]':'close'
  },
  setDatePicker: function(formName, tag, altFieldName){
    /*
     * Set datefields as a jquery datepicker
     */
    tag.datepicker({
      altField: "#" + formName + " input[name=" + altFieldName + "]",
      altFormat:"yy-mm-dd",
      dateFormat:"dd/mm/yy"
    });
    var date = this.model.get(altFieldName);
    if ((date !== null) && (date !== undefined)){
      date = parseDate(date);
      tag.datepicker('setDate', date);
    }
  },
  onBeforeClose:function(){
    /*
     *""" Reset the form before closing
     */
    this.reset();
  },
  onClose:function(){
    /*
     * """ Launched when the form view is closed : redirects to index
     */
    MyApp.router.navigate("index", {trigger: true});
  },
  reset: function(){
    /*
     * """ Reset the form (set all fields to blank)
     */
    resetForm(this.ui.form);
  }
});


Autonomie.addFormInitialize = function(options){
  /*
   * Custom add form initialization
   */
  this.destCollection = options['destCollection'];
  this.modelObject = options['modelObject'];
  this.model = new this.modelObject({});
  Backbone.Validation.bind(this);
};


Autonomie.editFormInitialize = function(options){
  /*
   * Custom edit form initialization
   */
  Backbone.Validation.bind(this);
};

Autonomie.addsubmit = function(e){
  /*
   *  Handle add form submissions
   */
  e.preventDefault();
  var this_ = this;
  var data = this.ui.form.serializeObject();
  // Here we need to use the model to which Backbone.Validation was bound in
  // the initialize method to launch validation, if not, the model dynamically
  // created below with destCollection.create has no validate method (that is
  // added when binding)
  if( ! this.model._validate(data, {validate:true})){
    return false;
  }
  this.destCollection.create(data,
    { success:function(){
        displayServerSuccess("Vos données ont bien été sauvegardées");
        Backbone.Validation.unbind(this_);
        this_.close();
       },
      error: function(){
        displayServerError("Une erreur a été rencontrée lors de la " +
          "sauvegarde de vos données");
      },
      wait:true,
      validate:true,
      sort:true}
  );
  Backbone.Validation.unbind(this);
  return false;
};
Autonomie.editsubmit =  function(e){
    var collection = this.model.collection;
    e.preventDefault();
    var this_ = this;
    var data = this.ui.form.serializeObject();
    this.model.save(data, {
      success:function(){
        collection.remove(this_.model);
        collection.add(this_.model);
        displayServerSuccess("Vos données ont bien été sauvegardées");
        Backbone.Validation.unbind(this_);
        this_.close();
      },
      error:function(model, xhr, options){
        displayServerError("Une erreur a été rencontrée lors de la " +
            "sauvegarde de vos données");
      },
      wait:true
    });
  Backbone.Validation.unbind(this);
  return false;
};
