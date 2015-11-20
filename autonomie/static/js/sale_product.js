var AppOptions = {};

var pp = Popup.extend({
  closefunc: function(){
    console.log("Not redirecting");
  },
  el: "#popup_container"
});

AutonomieApp.addRegions({
  categories: "#category_list",
  container: "#product_container",
  popup: pp
});

function initTiny(){
   /*
    * globally initialize TinyMCE
    * An editor can be added through
    *
    *    tinyMCE.execCommand('mceAddEditor', false, 'my_id_without_#');
    */
    tinyMCE.init({
      body_class: 'form-control',
      theme_advanced_toolbar_location: "top",
      theme_advanced_toolbar_align: "left",
      content_css: "/fanstatic/fanstatic/css/richtext.css",
      language: "fr_FR",
      plugins: ["lists", "searchreplace visualblocks fullscreen"],
      theme_advanced_resizing: true,
      height: "100px", width: 0,
      theme: "modern",
      strict_loading_mode: true,
      mode: "none",
      skin: "lightgray",
      menubar: false
    });
}

AutonomieApp.module('Product', function(Product, App, Backbone, Marionette, $, _){

  var CategoryModel = Backbone.Model.extend({
    validation: {
      title: {
        required: true,
        msg: "est requis"
      }
    },
    url: function(){
      if (this.get('id')){
        return AppOptions['contexturl'] + "/" + this.get('id');
      } else {
        return AppOptions['contexturl'];
      }
    },
    products_url: function(){
      return this.url() + "/products";
    },
    groups_url: function(){
      return this.url() + "/groups";
    }
  });

  var CategoryCollection = Backbone.Collection.extend({
    model: CategoryModel,
    comparator: "title"
  });

  var ProductModel = Backbone.Model.extend({
    validation: {
      label: {
        required: true,
        msg: "est requis"
      },
      value: function(value){
        if (isNaN(value) || ! ( transformToCents(value, 10) >= 0)){
          return "doit être un nombre positif";
        }
      }
    }
  });

  var ProductCollection = Backbone.Collection.extend({
    model: ProductModel,
    comparator: "label",
    initialize: function(models, options){
      this.url = options.url;
      this.category_id = options.category_id;
    }
  });

  var ProductGroupModel = Backbone.Model.extend({
    defaults: {
      'products': []
    },
    validation: {
      label: {
        required: true,
        msg: "est requis"
      }
    },
    addProduct: function(id, quantity) {
      var products = this.get('products');
      products.push({id: id, quantity: quantity});
    },
    item_url: function(){
      return this.url() + "/items";
    }
  });
  var ProductGroupItemModel = Backbone.Model.extend({
    /* M2M relationship objects between a group and a product with quantity */
    defaults: {
      'quantity': 1
    },
    validation: {
      quantity: {required: true, msg: 'est requise'}
    },
    url: function(){
      return this.collection.url;
    }
  });
  var ProductGroupItemCollection = Backbone.Collection.extend({
    /* Collection of products composing a group <-> M2M relationship objects */
    model: ProductGroupItemModel,
    initialize: function(models, options){
      this.url = options.url;
      this.product_group = options.product_group;
    },
    setDatas: function(options){
      var this_ = this;
      _.each(options.products, function(datas){
        var model = new ProductGroupItemModel(datas);
        model.set({sale_product_group_id: this_.product_group.get('id')});
        this_.add(model);
      });
    }
  });

  var ProductGroupCollection = Backbone.Collection.extend({
    model: ProductGroupModel,
    comparator: "label",
    initialize: function(models, options){
      this.url = options.url;
      this.category_id = options.category_id;
    }
  });

  var CategoryView = Marionette.ItemView.extend({
    template: "category",
    tagName: "li",
    className: "",
    modelEvents: {
      "change:title": "render"
    }
  });

  var CategoryListView = Marionette.CompositeView.extend({
    childView: CategoryView,
    template: "category_list",
    childViewContainer: "ul",
    set_active: function(category){
      this.children.each(function(view){
        if (view.model.cid == category.cid){
          view.$el.addClass('active');
        }else{
          view.$el.removeClass('active');
        }
      });
    }
  });

  var CategoryAddFormView = BaseFormView.extend({
    template: "category_form",
    ui: {
      form: "form"
    }
  });

  var MainLayoutView = Marionette.LayoutView.extend({
    template: "main_layout",
    regions: {
      title: '#category-title',
      products: '#product-list',
      groups: "#group-list"
    }
  });

  var CategoryEditView = CategoryAddFormView.extend({
    ui: {
      title: "h3 span",
      form: "form"
    },
    events: {
      "click button.edit": "showForm",
      'submit form': 'onFormSubmit',
      'click button.remove':'_remove'
    },
    showForm: function(){
      this.ui.form.toggle();
    },
    updateDatas: function(){
      this.ui.title.html(this.model.get('title'));
    },
    _remove: function(id){
      var this_ = this;
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cette catégorie (les produits et ouvrages seront également supprimés) ?");
      if (confirmed){
        var _model = this.model;
        _model.destroy({
          success: function(model, response) {
              this_.destroy();
              Product.router.navigate("index", {trigger: true});
              Product.router.controller.index();
              displayServerSuccess("L'élément a bien été supprimé");
            }
        });
      }
    },
    closeView: function(){
      this.ui.form.hide();
    }
  });

  var NoChildrenView = Marionette.ItemView.extend({
    template: "product_empty"
  });


  var ProductView = BaseTableLineView.extend({
    template: "product",
    tagName: "tr",
    events: {
      'click a.remove':'_remove',
      'click a.edit': 'showEditionForm'
    },
    modelEvents: {
      "change": "render"
    },
    _remove: function(id){
      var this_ = this;
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      if (confirmed){
        var _model = this.model;
        this.highlight({
          callback: function(){
            _model.destroy({
                success: function(model, response) {
                  this_.destroy();
                  displayServerSuccess("L'élément a bien été supprimé");
                }
             });
           }
          });
      }
    },
    templateHelpers: function(){
      var tva = this.model.get('tva');
      var current_tva = _.find(
        AppOptions['tvas'], function(item){return item.value == tva;}
      );
      var tva_label = "";
      if (!_.isUndefined(current_tva)){
        tva_label = current_tva.name;
      }
      return {tva_label: tva_label};
    },
    showEditionForm: function(){
      var product = this.model;
      controller.product_edit(product);
    }
  });

  var ProductListView = Marionette.CompositeView.extend({
    childView: ProductView,
    template: "product_list",
    emptyView: NoChildrenView,
    childViewContainer: "tbody",
    events: {
      "click a.add": "showAddForm"
    },
    showAddForm: function(){
      controller.add_product();
    }
  });

  var ProductFormView = BaseFormView.extend({
    template: "product_form",
    ui:{
      "form": "form"
    },
    focus: function(){
      this.ui.form.find('input').first().focus();
    },
    closeView: function(result){
      console.log("Closing the view");
      this.destroy();
    },
    templateHelpers: function(){
      var tva = this.model.get('tva');
      tva_options = this.updateSelectOptions(AppOptions['tvas'], tva);
      var unity = this.model.get('unity');
      unity_options = this.updateSelectOptions(
        AppOptions['unities'], unity);
      return {
        tva_options: tva_options,
        unity_options: unity_options
      };
    },
    onBeforeFormSubmit: function(){
      tinyMCE.triggerSave();
    },
    onShow: function(){
      // On détruit l'éditeur tinymce pour pouvoir en recréer un
      if (_.has(tinyMCE.editors, 'tiny_description') ){
        delete tinyMCE.editors.tiny_description;
      }
      tinyMCE.execCommand('mceAddEditor', false, 'tiny_description');
    }
  });
  /* PRODUCT GROUP VIEWS */
  var ProductGroupView = BaseTableLineView.extend({
    template: "product_group",
    events: {
      'click a.remove':'_remove',
      'click a.products': 'showItemList',
      'click a.edit': 'showEditionForm'
    },
    modelEvents: {
      "change": "render"
    },
    _remove: function(id){
      var this_ = this;
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      if (confirmed){
        var _model = this.model;
        this.highlight({
          callback: function(){
            _model.destroy({
                success: function(model, response) {
                  this_.destroy();
                  displayServerSuccess("L'élément a bien été supprimé");
                }
             });
           }
          });
      }
    },
    showItemList: function(){
      controller.product_group_item_list(this.model);
    },
    showEditionForm: function(){
      controller.product_group_edit(this.model);
    }
  });

  var ProductGroupListView = Marionette.CompositeView.extend({
    childView: ProductGroupView,
    template: "product_group_list",
    childViewContainer: "tbody",
    emptyView: NoChildrenView,
    events: {
      "click a.add": "showAddForm"
    },
    showAddForm: function(){
      controller.add_product_group();
    }
  });

  var ProductGroupItemView = BaseTableLineView.extend({
    template: "product_group_item",
    events: {
      'click a.remove':'_remove',
      'click a.edit': 'showEditionForm'
    },
    modelEvents: {
      "change": "render"
    },
    _remove: function(id){
      var this_ = this;
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet élément ?");
      if (confirmed){
        var _model = this.model;
        this.highlight({
          callback: function(){
            _model.destroy({
                success: function(model, response) {
                  this_.destroy();
                  displayServerSuccess("L'élément a bien été supprimé");
                }
             });
           }
          });
      }
    },
    showEditionForm: function(){
      controller.product_group_item_edit(this.model);
    }
  });

  var ProductGroupItemsView = Marionette.CompositeView.extend({
    childView: ProductGroupItemView,
    template: "product_group_item_list",
    childViewContainer: "tbody",
    emptyView: NoChildrenView,
    events: {
      'click button.close': "closeView",
      "click a.add": "showAddForm"
    },
    closeView: function(result){
      var this_ = this;
      this.$el.slideUp(400, function(){
        Backbone.history.loadUrl(Backbone.history.fragment);
        this_.destroy();
      });
    },
    showAddForm: function(){
      controller.add_product_group_item(this.options.product_group);
    }

  });

  var ProductGroupFormView = BaseFormView.extend({
    template: "product_group_form",
    events: {
      'click button.close': "closeView",
      'click button[name=submit]':'onFormSubmit',
      'click button[name=cancel]':'closeView',
      'submit form': 'onFormSubmit'
    },
    ui:{
      "form": "form"
    },
    toggleForm: function(){
      this.ui.form.toggle();
    },
    focus: function(){
      this.ui.form.find('input').first().focus();
    },
    closeView: function(result){
      var this_ = this;
      this.$el.slideUp(400, function(){
        Backbone.history.loadUrl(Backbone.history.fragment);
        this_.destroy();
      });
    },
    templateHelpers: function(){
      var title = "Ajout d'un ouvrage";
      if (! _.isUndefined(this.model.get('label'))){
        title = "Édition de l'ouvrage " + this.model.get('label');
      }
      return {
        form_title: title
      };
    }
  });

  var ProductGroupItemFormView = BaseFormView.extend({
    template: "product_group_item_form",
    events: {
      'click button.close': "closeView",
      'click button[name=submit]':'onFormSubmit',
      'click button[name=cancel]':'closeView',
      'submit form': 'onFormSubmit'
    },
    ui:{
      "form": "form",
      "select": "select[name=product_id]"
    },
    focus: function(){
      this.ui.form.find('input').first().focus();
    },
    closeView: function(result){
      var this_ = this;
      this.$el.slideUp(400, function(){
        // Backbone.history.loadUrl(Backbone.history.fragment);
        this_.destroy();
        controller.product_group_item_list(this_.destCollection.product_group);
      });
    },
    filter_options: function(item){
      /*
       * Filter values to avoid configuration of duplicate relationships
       * (sale_product_id/sale_product_group_id is used as mysql key)
       */
      // In edition mode, we allow the current item to be selected
      if (this.init_options.action === 'edit'){
        if (this.model.get('product_id') === item.id){
          return true;
        }
      }
      // else all products that are already associated to this group are
      // poped
      var index = _.indexOf(
        this.init_options.actual_product_ids,
        item.id);
      if (index !== -1){
        return false;
      }
      return true;
    },
    templateHelpers: function(){
      /*
       * Provide the available products for the group product item
       * add/edit form tmpl
       */
      _.bindAll(this, "filter_options");
      var options = this.init_options.products;

      options = _.filter(options, this.filter_options);

      var selected = this.model.get('product_id');
      if (! _.isUndefined(selected)){
        this.updateSelectOptions(options, selected, 'id');
      }
      return {product_options: options};
    },
    onRender: function(){
      this.ui.select.select2();
    }
  });

  var controller = {
    initialized:false,
    index: function(){
      this.initialize();
      App.container.empty();
      App.popup.empty();
      if (Product.categories.length === 1){
        this.category_edit(Product.categories.models[0].id);
      }
    },
    initialize: function(){
      if (! this.initialized){
        this.category_list_view = new CategoryListView(
          {collection: Product.categories}
        );
        App.categories.show(this.category_list_view);
      }
    },
    category_add: function(){
      var model = new CategoryModel({});

      this.category_add_view = new CategoryAddFormView({
        model: model, destCollection: Product.categories
      });

      App.container.show(this.category_add_view);
    },
    category_edit: function(id){
      var category = Product.categories.get(id);
      if (_.isUndefined(category)){
        Product.router.navigate('index', {trigger: true});
        return false;
      }
      this.category_list_view.set_active(category);
      this.current_category = category;
      this.main_layout = new MainLayoutView();
      App.container.show(this.main_layout);

      var category_title_view = new CategoryEditView({
        model: this.current_category, destCollection: Product.categories
      });
      this.main_layout.getRegion('title').show(category_title_view);

      this.product_collection = new ProductCollection(
        [],
        {url: category.products_url(), category_id: category.id}
      );

      var this_ = this;
      this.product_collection.fetch(
        {
          success: function(){
            var product_list_view = new ProductListView({
              collection: this_.product_collection
            });
            this_.main_layout.getRegion('products').show(product_list_view);
          }
        }
      );

      this.product_group_collection = new ProductGroupCollection(
        [],
        {url: category.groups_url(), category_id: category.id}
      );
      this.product_group_collection.fetch(
        {
          success: function(){
            var product_group_list_view = new ProductGroupListView({
              collection: this_.product_group_collection
            });
            this_.main_layout.getRegion('groups').show(
              product_group_list_view);
          }
        }
      );
      return true;
    },
    add_product: function(){
      var product = new ProductModel({});
      var add_form = new ProductFormView({
        model: product, destCollection: this.product_collection
      });
      App.popup.show(add_form);
    },
    product_edit: function(product){
      var edit_form = new ProductFormView({
        model: product, destCollection: this.product_collection
      });
      App.popup.show(edit_form);
      return true;
    },
    add_product_group: function(){
      var this_ = this;
      var product_group = new ProductGroupModel({});
      var add_form = new ProductGroupFormView({
        model: product_group,
        destCollection: this_.product_group_collection
      });
      App.popup.show(add_form);
    },
    product_group_edit: function(product_group){
      var this_ = this;
      var edit_form = new ProductGroupFormView({
        model: product_group,
        destCollection: this_.product_group_collection
      });
      App.popup.show(edit_form);
    },
    product_group_item_list: function(product_group){
      var this_ = this;
      this.product_group_item_collection = new ProductGroupItemCollection(
        [],
        {
          url: product_group.item_url(),
          product_group: product_group
        });
      product_group.fetch(
        {
          success: function(product_group, reponse, options){
            this_.product_group_item_collection.setDatas(
              {
                products: product_group.get('products')
              });
            var group_product_list_view = new ProductGroupItemsView({
              collection: this_.product_group_item_collection,
              product_group: product_group
            });
            App.container.show(group_product_list_view);
          }
        }
      );
    },
    add_product_group_item: function(product_group){
      var this_ = this;
      var product_group_item = new ProductGroupItemModel({
        sale_product_group_id: product_group.get('id')
      });
      // We load all products for the form, not only those from the current
      // category
      var load_all_products = initLoad(AppOptions['all_products_url']);
      load_all_products.then(
        function(result){
          var add_form = new ProductGroupItemFormView({
            model: product_group_item,
            destCollection: this_.product_group_item_collection,
            action: "add",
            actual_product_ids: _.pluck(
                product_group.get('products'),
                'id'),
            products: result.products
          });
          App.popup.show(add_form);
        }
      );
    },
    product_group_item_edit: function(product_group_item){
      var this_ = this;
      var load_all_products = initLoad(AppOptions['all_products_url']);
      var product_group = this.product_group_collection.get(product_group_item.get('sale_product_group_id'));
      load_all_products.then(
        function(result){
          var edit_form = new ProductGroupItemFormView({
            model: product_group_item,
            destCollection: this_.product_group_item_collection,
            action: "edit",
            products: result.products,
            actual_product_ids: _.pluck(
                product_group.get('products'),
                'id')
          });
          App.popup.show(edit_form);
        }
      );
    }
  };

  var router = Backbone.Marionette.AppRouter.extend({
    controller: controller,
    appRoutes: {
      "index": "index",
      "categories/:id/edit": "category_edit",
      "categories/add": "category_add"
    }
  });

  Product.on('start', function(){
    var datas = Product.datas;
    Product.categories = new CategoryCollection(datas['categories']);
    Product.categories.url = AppOptions['contexturl'];
    Product.router = new router();
    Product.router.controller.index();
  });

});

function ProductPageInit(options){
  if (AppOptions['loadurl'] !== undefined){
    // page statistic
    var module = AutonomieApp.module('Product');
    // Quand on start on lance initModule en callback de la requête jquery
    var options_load = initLoad(AppOptions['loadurl']).then(
      function(data){
        _.extend(AppOptions, data);
      }
    );
    var categories_load = initLoad(AppOptions['contexturl']);
    categories_load.then(function(datas){
      module.datas = datas;
    });
    $.when(options_load, categories_load).then(
      function(datas){
        AutonomieApp.start();
      }
    );
  }
}
$(function(){
  ProductPageInit();
  initTiny();
});
