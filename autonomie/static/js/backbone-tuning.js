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
Backbone.Marionette.Renderer.render = function(template_name, data){
  var template_obj = Handlebars.templates[template_name + '.mustache'];
  return template_obj(data);
};


var Autonomie = {};


// Provide a default table item view
var BaseTableLineView = Backbone.Marionette.ItemView.extend({
  highlight: function( options ){
    /*
     * Ok highlight
     */
    if (options['scroll']){
      this._scroll();
    }
    this._highlight("#ceff99", options['callback']);
  },
  error: function(callback){
    /*
     * Error highlight
     */
    this._highlight("#F9AAAA", callback);
  },
  _scroll: function(){
    var top = this.$el.offset().top - 50;
    $('html, body').animate({scrollTop: top});
  },
  _highlight: function(color, callback){
    /*
     * scroll to the view, highlight with the given color and launch the
     * callback
     */
    // Silly hack to provide highlights on webkit browsers
    this.$el.css("backgroundColor", "#fff");
    this.$el.effect('highlight', {color:color}, 1500,
                    function(){if (callback !== undefined){ callback();}
                });
  }
});
var BaseFormView = Backbone.Marionette.CompositeView.extend({
  /*
   *
   * Base form view, provides base structure for adding/editing elements.
   *
   *  * It validates the fields regarding the model that have been passed
   *  * It adds a model to a provided destCollection on submission or saves it in
   * case of edition
   *  * It provides tools to handle jquery datepickers
   *
   *  A class extending this one should at least provide:
   *   a ui object as attribute with a css selector pointing the form object
   *   a template attribute
   *
   */
  events: {
    'click button[name=submit]':'onFormSubmit',
    'click button[name=cancel]':'close'
  },
  initialize: function(options){
    // In case of add forms, we need to pass a dest collection that will be
    // used on submission
    if (! _.isUndefined(options['destCollection'])){
      this.destCollection = options['destCollection'];
    }
    if (! _.isUndefined(options['model'])){
      // A model was passed on view creation
      this.listenTo(this.model, 'change', this.render, this);
    }
  },
  setDatePicker: function(formName, tag, altFieldName, today){
    /*
     * Set datefields as a jquery datepicker
     */
    var altField = "#" + formName + " input[name=" + altFieldName + "]";
    tag.datepicker({
      altField: altField,
      altFormat:"yy-mm-dd",
      dateFormat:"dd/mm/yy"
    });
    var date = this.model.get(altFieldName);
    if ((date !== null) && (! _.isUndefined(date))){
      date = parseDate(date);
      tag.datepicker('setDate', date);
    }else{
      if (! _.isUndefined(today)){
        date = parseDate(today);
        tag.datepicker('setDate', date);
      }
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
  },
  formDatas: function(){
    return this.ui.form.serializeObject();

  },
  addSubmit: function(){
    /*
     * Called when adding an element
     */

    // Collection.create doesn't fire the validation, we need to set datas to
    // our model before'
    this.model.set(this.formDatas(), {validate:true});

    if (! this.model.isValid() ){
      Backbone.Validation.unbind(this);
      return false;
    }

    // We now add the item to the dest collection
    var this_ = this;
    this.destCollection.create(
      this.model,
      {
        success:function(){
          displayServerSuccess("Vos données ont bien été sauvegardées");
          Backbone.Validation.unbind(this_);
          this_.close();
        },
        error: function(){
          displayServerError("Une erreur a été rencontrée lors de la " +
            "sauvegarde de vos données");
        },
        wait:true,
        sort:true
      }
    );
    return true;
  },
  editSubmit: function(){
    /*
     * Called on element edition
     */
    // When saving, the datas are validated, and a change event is fired
    var this_ = this;
    var collection = this.model.collection;
    this.model.save(
      this.formDatas(),
      {
        success:function(){
          // On adding an element :
          //  * the collection is sorted
          //  * the html output is placed at the good place in the table
          //
          // Here we force our element to be re-rendered (if the date changed)
          // This way the element is also highlighted
          //  Here we comment this specific point it doesn't work as expected
          //
//          collection.remove(this_.model);
//          collection.add(this_.model);

          displayServerSuccess("Vos données ont bien été sauvegardées");
          Backbone.Validation.unbind(this_);
          // When closing it's as we called return (next code is not called)
          this_.close();
        },
        error:function(model, xhr, options){
          displayServerError("Une erreur a été rencontrée lors de la " +
              "sauvegarde de vos données");
        },
        wait:true
      }
    );

  },
  onFormSubmit: function(e){
    Backbone.Validation.bind(this);
    e.preventDefault();
    var this_ = this;


    if (this.model.isNew()){
      // Adding an element
      this.addSubmit();
    } else {
      // Editing an element
      this.editSubmit();
    }
    Backbone.Validation.unbind(this);
    return true;
  }
});


Autonomie.addFormInitialize = function(options){
  /*
   * Custom add form initialization
   */
};


Autonomie.editFormInitialize = function(options){
  /*
   * Custom edit form initialization
   */
};

Autonomie.addsubmit = function(e){
  /*
   *  Handle add form submissions
   */
  e.preventDefault();
  var this_ = this;
  // We get a clone of the attributes passed to our current model
  // In order not to affect the model when extending the "data" object
  var data = _.clone(this.model.attributes);

  var form_datas = this.ui.form.serializeObject();

  _.extend(data, form_datas);

  // Here we need to use the model to which Backbone.Validation was bound in
  // the initialize method to launch validation, if not, the model dynamically
  // created below with destCollection.create has no validate method (that is
  // added when binding)
//  if( ! this.model._validate(data, {validate:true})){
//    return false;
//  }
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
