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



var AppOptions = {};


var pp = Popup.extend({
  el:'#form-container'
});


AutonomieApp.addRegions({
  /*
   * Application regions
   */
  linesRegion:'#expenses',
  linesKmRegion:'#expenseskm',
  formContainer: pp,
  headerContainer: '#header-container'
});


AutonomieApp.module("Expense", function(Expense, AutonomieApp,  Backbone, Marionette, $, _){
  /******************************** Models ********************************/
  var BookMarkModel = Backbone.Model.extend({
    initialize: function(options){
      var type_id = options['type_id'];
      if (! _.isUndefined(type_id)){
        this.set('type', this.getType(type_id));
      }
    },
    getType: function(type_id){
      return _.find(AppOptions['expense_types'], function(type){return type['value'] == type_id;});
    }
  });

  var BookMarksCollection = Backbone.Collection.extend({
    url: "/bookmarks",
    model: BookMarkModel
  });

  var BaseExpenseModel = Backbone.Model.extend({
    /*
     * BaseModel for expenses, provides tools to access main options
     */
    getTypeOption:function(arr){
      /*
       * Retrieve the element from arr where its type_id is the same as the model's
       * current one
       */
      var type_id = this.get('type_id');
      return _.find(arr, function(type){return type['value'] == type_id;});
    },
    getTypeOptions: function(){
      /*
       * Return an array of options for types ( should be overriden )
       */
      return [];
    },
    getType: function(){
      /*
       * return the type object associated to the current model
       */
      var options = this.getTypeOptions();
      return this.getTypeOption(options);
    },
    getTypeLabel: function(){
      /*
       * Return the Label of the current type
       */
      var current_type = this.getType();
      var options = this.getTypeOptions();
      if (current_type === undefined){
        return "";
      }else{
        return current_type.label;
      }
    }
  });

  var ExpenseLine = BaseExpenseModel.extend({
    /*
     *  Expenseline model
     *
     *  An expense line should be a tel expense or a more general one
     *
     *  It's composed of HT value, TVA value, description, expensetype id, date
     *
     *  altdate is used for display
     */
    // default values for an expenseline
    defaults:{
      category: null,
      description:"",
      ht:null,
      tva:null
    },
    // Constructor dynamically add a altdate if missing
    // (altdate is used in views for jquery datepicker)
    initialize: function(options){
      if ((options['altdate'] === undefined)&&(options['date']!==undefined)){
        this.set('altdate', formatPaymentDate(options['date']));
      }
    },
    // Validation rules for our model's attributes
    validation:{
      category: {
        required:true,
        msg:"est requise"
      },
      type_id:{
        required:true,
        msg:"est requis"
      },
      date: {
        required:true,
        pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
        msg:"est requise"
      },
      ht: {
        required:true,
        // Match"es 19,6 19.65 but not 19.654"
        pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
        msg:"doit être un nombre"
      },
      tva: {
        required:true,
        pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
        msg:"doit être un nombre"
      }
    },
    total: function(){
      var total = this.getHT() + this.getTva();
      if (this.isSpecial()){
        var percentage = this.getTypeOption(AppOptions['expensetel_types']).percentage;
        total = getPercent(total, percentage);
      }
      return total;
    },
    getTva:function(){
      return parseFloat(this.get('tva'));
    },
    getHT:function(){
      return parseFloat(this.get('ht'));
    },
    isSpecial:function(){
      /*
       * return True if this expense is a special one (related to phone)
       */
      return this.getTypeOption(AppOptions['expensetel_types']) !== undefined;
    },
    hasNoType: function(){
      var isnottel = _.isUndefined(this.getTypeOption(AppOptions['expensetel_types']));
      var isnotexp = _.isUndefined(this.getTypeOption(AppOptions['expense_types']));
      if (isnottel && isnotexp){
        return true;
      }else{
        return false;
      }
    },
    getTypeOptions: function(){
      var arr;
      if (this.isSpecial()){
        arr = AppOptions['expensetel_types'];
      }else{
        arr = AppOptions['expense_types'];
      }
      return arr;
    }
  });


  var ExpenseKmLine = BaseExpenseModel.extend({
    /*
     *  Model for expenses related to kilometers fees
     *
     *  Km fees are compound of :
     *  * kilometers
     *  * expense type id
     *  * start point
     *  * end point
     *  * description
     *
     */
    defaults:{
      category:null,
      start:"",
      end:"",
      description:""
    },
    initialize: function(options){
      if ((options['altdate'] === undefined)&&(options['date']!==undefined)){
        this.set('altdate', formatPaymentDate(options['date']));
      }
    },
    validation:{
      category: {
        required:true,
        msg:"est requise"
      },
      type_id:{
        required:true,
        msg:"est requis"
      },
      date: {
        required:true,
        pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
        msg:"est requise"
      },
      km: {
        required:true,
        // Match"es 19,6 19.65 but not 19.654"
        pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
        msg:"doit être un nombre"
      }
    },
    getIndice: function(){
      /*
       *  Return the reference used for compensation of km fees
       */
      var elem = _.where(AppOptions['expensekm_types'], {value:this.get('type_id')})[0];
      if (elem === undefined){
        return 0;
      }
      return parseFloat(elem.amount);
    },
    total: function(){
      var km = this.getKm();
      var amount = this.getIndice();
      return km * amount;
    },
    getKm:function(){
      return parseFloat(this.get('km'));
    },
    getTypeOptions: function(){
      return AppOptions['expensekm_types'];
    }
  });

  var ExpenseLineCollection = Backbone.Collection.extend({
    /*
     *  Collection of expense lines
     */
    model: ExpenseLine,
    url: "/expenses/lines",
    comparator: function( a, b ){
      /*
       * Sort the collection and place special lines at the end
       */
      var res = 0;
      if ( b.isSpecial() ){
        res = -1;
      }else if( a.isSpecial() ){
        res = 1;
      }else{
        var acat = a.get('category');
        var bcat = b.get('category');
        if ( acat < bcat ){
          res = -1;
        }else if ( acat > bcat ){
          res = 1;
        }
        if (res === 0){
          var adate = a.get('altdate');
          var bdate = a.get('altdate');
          if (adate < bdate){
            res = -1;
          } else if ( acat > bcat ){
            res = 1;
          }
        }
      }
      return res;
    },
    total: function(category){
      /*
       * Return the total value
       */
      var result = 0;
      this.each(function(model){
        if (category != undefined){
          if (model.get('category') != category){
            return;
          }
        }
        result += model.total();
      });
      return result;
    }
  });

  var ExpenseKmCollection = Backbone.Collection.extend({
    /*
     * Collection for expenses related to km fees
     */
    model: ExpenseKmLine,
    total: function(category){
      var result = 0;
      this.each(function(model){
        if (category != undefined){
          if (model.get('category') != category){
            return;
          }
        }
        result += model.total();
      });
      return result;
    }
  });

  var ExpenseSheet = Backbone.Model.extend({
    /*
     *  Main expense sheet model
     */
    urlRoot:"/expenses/",
    initialize: function(options){
      this.lines = new ExpenseLineCollection(options['lines']);
      this.lines.url = this.urlRoot + this.id + "/lines";
      this.kmlines = new ExpenseKmCollection(options['kmlines']);
      this.kmlines.url = this.urlRoot + this.id + "/kmlines";
    }
  });

////////////////////////////////////////////////////////////////
/********************  Views  *********************************/
////////////////////////////////////////////////////////////////
  var BaseExpenseLineView = BaseTableLineView.extend({
    /*
     * Base item view for expense lines
     */
    _remove: function(){
      /*
       *  Delete the line
       */
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      if (confirmed){
        var _model = this.model;
        this.highlight({
          callback: function(){
            _model.destroy({
                success: function(model, response) {
                  displayServerSuccess("L'élément a bien été supprimé");
                }
             });
           }
          });
      }
    }
  });

  var ExpenseLineView = BaseExpenseLineView.extend({
    /*
     *  Expense Line view (for classic and tel expenses)
     */
    tagName:"tr",
    events: {
      'click a.remove':'_remove',
      'change input[name=ht]':'changeVal',
      'change input[name=tva]':'changeVal'
    },
    ui:{
      htinput:'input[name=ht]',
      tvainput:'input[name=tva]',
      total:'span[class=total]'
    },
    templateHelpers:function(){
      /*
       * Add custom var for rendering
       */
      var this_ = this;
      var typelabel = function(){
        return this_.model.getTypeLabel();
      };

      var edit_url = "#lines/" + this.model.cid + "/edit";
      var bookmark_url = "#lines/" + this.model.cid + "/bookmark";
      var total = this.model.total();
      return {typelabel:typelabel,
              edit_url:edit_url,
              bookmark_url: bookmark_url,
              total:formatAmount(total),
              edit:AppOptions['edit']
              };
    },
    getTemplate: function(){
      /*
       * Return the template used
       */
      if (this.model.hasNoType()){
        return "expenseorphan"; //templates.expenseorphan;
      }
      if (this.model.isSpecial()){
        return "expensetel";
      }

      return "expense";
    },
    initialize: function(){
      /*
       * View constructor
       */
      // bind the model change to the view rendering
      if (! this.model.isSpecial()){
        this.listenTo(this.model, 'change', this.render, this);
        this.listenTo(this.model, 'change', this.highlight, this);
      }
    },
    changeVal: function(){
      /*
       * Called when one of the inputs have been edited
       */
      Backbone.Validation.bind(this);
      var this_ = this;
      var attrs = { ht:this.ui.htinput.val(), tva:this.ui.tvainput.val()};
      this.model.save(attrs, {
            success:function(){
              displayServerSuccess("Les informations ont bien été enregistrées");
              this_.setTotal();
            },
            error:function(){
              displayServerError("Une erreur est survenue lors la sauvegarde" +
              " de vos données. Contactez votre administrateur.");
            },
            wait:true});
      Backbone.Validation.unbind(this);
    },
    setTotal: function(){
      var total = this.model.total();
      total = formatAmount(total);
      this.ui.total.html(total);
    }
  });

  var ExpenseKmLineView = BaseExpenseLineView.extend({
    /*
     *  View for expenses related to km fees
     */
    template: "expenseKm",
    tagName:"tr",
    events: {
      'click a.remove':'_remove'
    },
    templateHelpers:function(){
      /*
       *  Load dynamic datas for rendering
       */
      var typelabel = this.model.getTypeLabel();
      var total = this.model.total();
      var edit_url = "#kmlines/" + this.model.cid + "/edit";
      return {
              typelabel:typelabel,
              edit_url:edit_url,
              edit:AppOptions['edit'],
              total:formatAmount(total)
              };
    },
    initialize: function(){
      this.listenTo(this.model, 'change', this.render, this);
    }
  });

  var BaseExpenseCollectionView = Backbone.Marionette.CompositeView.extend({
    /*
     * A base expense collection View
     *
     * It provides two tables : one for internal and another for activity related
     * expenses
     */
    tagName: "div",
    internalContainer: "tbody.internal",
    activityContainer: "tbody.activity",
    templateHelpers:function(){
      return {edit:AppOptions['edit']};
    },
    attachHtml: function(collectionView, childView, index){
      /*
       * Choose the container for child appending regarding the category
       */

      // Subscribe to the change behaviour of our model
      this.listenTo(childView.model, 'change', this.setTotal, this);
      this.listenTo(childView.model, 'change:category', this.render, this);

      var childrenContainer;
      // Retrieve the container our expense should be rendered in
      if (childView.model.get('category') == '1'){
        // It's an expense related to internal needs
        childrenContainer = collectionView.$(collectionView.internalContainer);
      }else{
        // It's an expense related to the company's activity
        childrenContainer = collectionView.$(collectionView.activityContainer);
      }
      this.appendChild(index, childView, childrenContainer);

      // Highight a newly added element
      if (_.isFunction(childView.highlight)){
        // The new_element attribute is used to check if we should highlight(on
        // add only)
        var options = {};
        if (childView.model.has('new_element')){
          options['scroll'] = true;
          childView.model.unset('new_element', {silent:true});
        }
        childView.highlight(options);
        }
    },
    appendChild: function(index, childView, childrenContainer){
      childrenContainer.append(childView.el);
    },
    onRender: function(collectionView){
      this.setTotal();
    },
    onItemRemoved: function(){
      this.setTotal();
    },
    onAfterItemAdded: function(){
      this.setTotal();
    },
    setTotal: function(){
      /*
       * Set the total value for the current collection
       */
      AutonomieApp.vent.trigger("expense.totalchanged");
      this.ui.internalTotal.html(formatAmount(this.collection.total('1')));
      this.ui.activityTotal.html(formatAmount(this.collection.total('2')));
    }
  });

  var ExpensesView = BaseExpenseCollectionView.extend({
    /*
     *  CompositeView that presents the expenses collection in a table
     */
    template: "expenseList",
    childView: ExpenseLineView,
    id: "expenselines",
    ui:{
      internalTotal:'#internal_total',
      activityTotal:'#activity_total'
    },
    appendChild: function(index, childView, childrenContainer){
      var children = childrenContainer.children();
      if (children.size() <= index) {
        childrenContainer.append(childView.el);
      } else {
        childrenContainer.children().eq(index).before(childView.el);
      }
    }
  });

  var ExpensesKmView = BaseExpenseCollectionView.extend({
    /*
     *  CompositeView that presents the expenses related to km fees in a table
     */
    template: "expenseKmList",
    childView: ExpenseKmLineView,
    id:'expensekmlines',
    ui:{
      internalTotal:'#km_internal_total',
      activityTotal:'#km_activity_total'
    }
  });

  ////////////////////////////////////////
  // FormViews
  ////////////////////////////////////////

  var BaseExpenseFormView = BaseFormView.extend({
    formselector: null,
    templateHelpers: function(){
      /*
       * Add datas to the template context
       */
      var this_ = this;
      return {
        bookmark_options: function(){
          return Expense.bookmarks.toArray();
        },
        type_options: function(){
          return this_.getTypeOptions();
        },
        category_options: function(){
          return this_.getCategoryOptions();
          }
        };
    },
    onShow: function(){
       //Called when added to the DOM by the région
      this.setDatePicker(this.forname, this.ui.date, "date", AppOptions['today']);
    },
    onRender: function(){
      // Called when rendered (the first time the setDatePicker doesn't work
      // because the datas is rendered but not added to the DOM, that's why the
      // call is also made in onShow)
      this.setDatePicker(this.formselector, this.ui.date, "date", AppOptions['today']);
      if (!_.isUndefined(this.ui.bookmarks)){
        this.setBookMarkBehaviour();
      }
    },
    setBookMarkBehaviour: function(){
      /*
       * Add the bookmark select's behaviour
       */
      _.bindAll(this, "updateFormWithBookMark", "deleteBookmark");
      var this_ = this;
      this.ui.bookmarks.find('a.edit').unbind('click.usebookmark');
      this.ui.bookmarks.find('a.edit').bind('click.usebookmark', function(){
        var cid = $(this).attr('data-cid');
        this_.updateFormWithBookMark(cid);
      });
      this.ui.bookmarks.find('a.delete').unbind('click.deletebookmark');
      this.ui.bookmarks.find('a.delete').bind(
        'click.deletebookmark',
        function(){
          var cid = $(this).attr('data-cid');
          this_.deleteBookmark(cid);
        }
      );
    },
    updateFormWithBookMark: function(cid){
      /*
       * Update the form models regarding the selected bookmark
       */
      if (_.isUndefined(cid)){
        return false;
      }
      var bookmark = Expense.bookmarks.get(cid);
      var model = this.model;

      _.each(['type_id', 'description', 'ht', 'tva'], function(key){
        model.set(key, bookmark.get(key));
      });
      return true;
    },
    deleteBookmark: function(cid){
      if (_.isUndefined(cid)){
        return false;
      }
      var bookmark = Expense.bookmarks.get(cid);
      var this_ = this;
      bookmark.destroy({
        success: function(model, response) {
          displayServerSuccess("Le favori a bien été supprimé");
          this_.render();
        }
      });
      return true;
    }
  });

  var ExpenseFormView = BaseExpenseFormView.extend({
    template: "expenseForm",
    formselector: "#expenseForm",
    ui:{
      form:"#expenseForm",
      date:"#expenseForm input[name=altdate]",
      bookmarks: "#expenseForm #bookmarks"
    },
    getCategoryOptions:function(){
      var category_options = AppOptions['categories'];
      var category = this.model.get('category');
      return this.updateSelectOptions(category_options, category);
    },
    getTypeOptions: function(){
      var type_options = _.where(AppOptions['expense_types'], {active: true});
      var type_id = this.model.get('type_id');
      return this.updateSelectOptions(type_options, type_id);
    }
  });

  var ExpenseKmFormView = BaseExpenseFormView.extend({
    template: "expenseKmForm",
    formselector: "#expenseKmForm",
    ui:{
      form:"#expenseKmForm",
      date:"#expenseKmForm input[name=altdate]"
    },
    getCategoryOptions:function(){
      var category_options = AppOptions['categories'];
      var category = this.model.get('category');
      return this.updateSelectOptions(category_options, category);

    },
    getTypeOptions: function(){
      var type_options = _.where(AppOptions['expensekm_types'], {active: true});
      var type_id = this.model.get('type_id');
      return this.updateSelectOptions(type_options, type_id);
    }
  });

  var ExpenseTelFormView = BaseFormView.extend({
    template: "expenseTelForm",
    ui:{
      form:"#expenseTelForm"
    },
    templateHelpers: function(){
      return {
        type_options: _.where(AppOptions['expensetel_types'], {active: true})
      };
    }
  });

  var controller = {
    /*
     * App controller
     */
    initialized:false,
    _popup:null,
    lines:null,
    kmlines:null,
    index: function() {
      this.ensurePopupClosed();
      this.initialize();
    },
    ensurePopupClosed: function(){
      /*
       *  ensure the popup is closed (is necessary when we come from other views)
       */
      AutonomieApp.formContainer.closeModal();
    },
    initialize:function(){
      if (!this.initialized){
        this.lines = new ExpensesView({collection: Expense.expense.lines});
        this.kmlines = new ExpensesKmView( {collection: Expense.expense.kmlines});

        AutonomieApp.linesRegion.show(this.lines);
        AutonomieApp.linesKmRegion.show(this.kmlines);
        this.initialized = true;
      }
    },
    _getExpenseLine:function(id){
      /*
       * Return the expenseline by id or cid
       */
      var model = Expense.expense.lines.get(id);
      return model;
    },
    _getExpenseKmLine:function(id){
      /*
       * Return the expenseKmline by id or cid
       */
      var model = Expense.expense.kmlines.get(id);
      return model;
    },
    add: function(category){
      /*
       * expenseline add route
       */
      this.initialize();
      // Passing the new_element tags a creation used to highlight (or not) the
      // line
      var model = new ExpenseLine({"category": category, new_element: true});
      var expense_form = new ExpenseFormView({
        title: "Ajouter",
        destCollection: Expense.expense.lines,
        model: model
      });
      AutonomieApp.formContainer.show(expense_form);
    },
    edit: function(id) {
      /*
       * expenseline edit route
       */
      this.initialize();
      var model = this._getExpenseLine(id);
      var expense_form = new ExpenseFormView({
        title:"Modifier",
        destCollection: Expense.expense.lines,
        model:model
        });
      AutonomieApp.formContainer.show(expense_form);
    },
    bookmark: function(id){
      this.initialize();
      var model = this._getExpenseLine(id);
      // Get only the attributes necessary for our bookmark
      var attributes = _.pick(model.attributes,
                          "type_id", "description", "ht", "tva" );

      var bookmark = new BookMarkModel(attributes);
      Expense.bookmarks.create(bookmark, {
          'success':function(){
            displayServerSuccess("L'élément a bien été ajouté à vos favoris");
            Expense.router.navigate("index", {trigger: true});
          },
          'error': function(){
            displayServerError("Erreur à l'ajout de favoris");
            Expense.router.navigate("index", {trigger: true});
          }
        }
      );
    },
    addtel: function(){
      this.initialize();
      // Passing the new_element tags a creation used to highlight (or not) the
      // line
      var model = new ExpenseLine({
        category: "1",
        new_element: true,
        date: AppOptions['today']
        });
      var expensetel_form = new ExpenseTelFormView({
        title:'Ajouter des frais téléphoniques',
        destCollection:Expense.expense.lines,
        model: model
      });
      console.log(expensetel_form);
      AutonomieApp.formContainer.show(expensetel_form);
    },
    addkm: function(category){
      this.initialize();
      // Passing the new_element tags a creation used to highlight (or not) the
      // line
      var model = new ExpenseKmLine({new_element: true, category: category});
      var expensekm_form = new ExpenseKmFormView({
        title:"Ajouter",
        destCollection:Expense.expense.kmlines,
        model: model
      });
      AutonomieApp.formContainer.show(expensekm_form);
    },
    editkm: function(id) {
      this.initialize();
      var model = this._getExpenseKmLine(id);
      var expensekm_form = new ExpenseKmFormView({
        title:"Modifier",
        model:model
      });
      AutonomieApp.formContainer.show(expensekm_form);
    },
    print: function(){
      window.print();
    }
  };

  var router = Backbone.Marionette.AppRouter.extend({
    /*
     *  Local route configuration
     *
     *  Link the routes to a named method that should be provided by one of the
     *  controllers
     */
    controller: controller,
    appRoutes: {
      "index":"index",
      "lines/:id/edit": "edit",
      "lines/:id/bookmark": "bookmark",
      "lines/add/:category": "add",
      "lines/add": "add",
      "tel/add": "addtel",
      "kmlines/:id/edit": "editkm",
      "kmlines/add/:category": "addkm",
      "kmlines/add": "addkm",
      "print": "print"
    }
  });

  var updateTotal = function(){
      var text = "Total des frais professionnels à payer : ";
      var total = Expense.expense.lines.total() +  Expense.expense.kmlines.total();
      text += formatAmount(total);
      $('#total').html(text);
  };

  Expense.on('start', function(){
    /*
     * Initialize the module's datas
     */
    var data = Expense.datas;
    Expense.router = new router();
    _.extend(AppOptions, data['options']);
    Expense.expense = new ExpenseSheet(data['expense']);
    Expense.bookmarks = new BookMarksCollection(AppOptions['bookmarks']);
    Expense.router.controller.index();

    // Setup the event listening
    AutonomieApp.vent.on("expense.totalchanged", updateTotal);
    updateTotal();
  });
});

$(function(){
  var ajax_call = initLoad(AppOptions['loadurl']);
  ajax_call.then(function(datas){
    AutonomieApp.module('Expense').datas = datas;
    AutonomieApp.start();
  });
});
