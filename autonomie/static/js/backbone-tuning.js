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


var LazyLoadedOptions = Backbone.Marionette.Object.extend({
  /*
   * Allow lazy loading of options
   *
   * var options = new LazyLoadedOptions({
   *      url: 'myurl',
   *      values: {'preloadedoptions'},
   *      keywork: 'mycustomkey'
   *  });
   * options.load('option1'); // Load the key from the server passing {mycustomkey: 'option1'}
   *
   * options.load('option1'); // Returns the previously sended request
   */
  initialize: function(options){
    this.options = options.values || {};
    this.url = options.url;
    this.keyword = options.keyword || 'key';
  },
  load: function(key){
    var result;
    var cached_value = this.options[key];

    if (_.isUndefined(cached_value)){
      var this_ = this;
      var raw_datas = {};
      raw_datas[this.keyword] = key;
      var datas = JSON.stringify(raw_datas);
      this.locked = true;
      result = $.ajax({
          url: this.url,
          data: datas,
          contentType:'application/json',
          dataType: 'json',
          method: 'POST',
          success: function(result){
            // We store the result in the cache
            this_.options[key] = result.options;
          },
          error: function(result){
            alert("'Une erreur est survenue au chargement d'une clé'. " +
            "Contacter un administrateur");
          }
        });
    } else {
      // On renvoie une "promise" un truc sur lequel on peut caller des
      // callbacks comme sur une requête ajax
      var def = $.Deferred();
      result = def.done(function(){return cached_value;});
      def.resolve();
    }
    return result;
  }
});


var AutonomieApp = new Backbone.Marionette.Application();

var controller = {
  appindex: function(){
  }
};

var MainRouter = Backbone.Marionette.AppRouter.extend({
  controller: controller,
  appRoutes: {
    "": "appindex"
  }
});

AutonomieApp.on("start", function(){
  /*
   *""" Launche the history (controller and router stuff)
   */
  AutonomieApp.router = new MainRouter();
  Backbone.history.start();
});

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
    'click button[name=cancel]':'closeView',
    'submit form': 'onFormSubmit'
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
    _.bindAll(this, ['closeView']);
  },
  setDatePicker: function(formSelector, tag, altFieldName, today){
    /*
     * Set datefields as a jquery datepicker
     */
    var altField = formSelector + " input[name=" + altFieldName + "]";
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
    AutonomieApp.router.navigate("index", {trigger: true});
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
  closeView:function (result){
    /*
     * Default close view behaviour
     */
    this.destroy();
    AutonomieApp.router.navigate("index", {trigger: true});
  },
  addSubmit: function(){
    /*
     * Called when adding an element
     */
    // Collection.create doesn't fire the validation, we need to set datas to
    // our model before'
    this.model.set(this.formDatas(), {validate:true});

    if (! this.model.isValid() ){
      return false;
    }
    // We now add the item to the dest collection
    var this_ = this;
    this.destCollection.create(
      this.model.toJSON(),
      {
        success:function(result){
          displayServerSuccess("Vos données ont bien été sauvegardées");
          this_.closeView(result);
        },
        error: function(){
          displayServerError("Une erreur a été rencontrée lors de la " +
            "sauvegarde de vos données");
        },
        sort:true,
        wait: true
      }
    );
    return true;
  },
  editSubmit: function(result){
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
          displayServerSuccess("Vos données ont bien été sauvegardées");
          this_.closeView(result);
        },
        error:function(model, xhr, options){
          displayServerError("Une erreur a été rencontrée lors de la " +
              "sauvegarde de vos données");
        },
        wait: true
      }
    );

  },
  onFormSubmit: function(e){
    e.preventDefault();
    Backbone.Validation.bind(this);
    var this_ = this;


    if (! this.model.get('id')){
      // Adding an element
      this.addSubmit();
    } else {
      // Editing an element
      this.editSubmit();
    }
    Backbone.Validation.unbind(this);
    return true;
  },
  updateSelectOptions: function(options, val){
    /*
     * Add the selected attr to the option with value 'val'
     */
    if (!_.isArray(val)){
      val = [val];
    }
    _.each(options, function(option){
      delete option['selected'];
      if (_.contains(val, option['value'])){
        option['selected'] = 'true';
      }
    });
    return options;
  }
});

function initLoad(url){
  /*
   * Load function ideal for module initialization
   *
   * :param url: The url to load
   */
  return $.ajax({
    url:url,
    dataType: 'json',
    mimeType: "textPlain",
    data: {},
    cache: false,
    error: function(){
      alert("Une erreur a été rencontrée, contactez votre administrateur.");
    }
  });
}
