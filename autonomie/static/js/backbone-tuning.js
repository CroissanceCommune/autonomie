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
