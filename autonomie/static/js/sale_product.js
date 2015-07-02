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
    }
  });

  var CategoryCollection = Backbone.Collection.extend({
    model: CategoryModel
  });

  var ProductModel = Backbone.Model.extend({
    validation: {
      label: {
        required: true,
        msg: "est requis"
      },
      value: function(value){
        if (isNaN(value) || ! ( parseInt(value, 10) >= 0)){
          return "doit être un nombre positif";
        }
      }
    }
  });

  var ProductCollection = Backbone.Collection.extend({
    model: ProductModel,
    comparator: "label",
    initialize: function(options){
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
    childViewContainer: "ul"
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
      list: '#product-list'
    },
    events: {
      'click button.close': "closeView"
    },
    closeView: function(){
      var this_ = this;
      this.$el.slideUp(400, function(){
        this_.destroy();
        AutonomieApp.router.navigate("index", {trigger: true});
      });
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
      console.log("Showform");
      console.log(this.ui);
      this.ui.form.toggle();
    },
    updateDatas: function(){
      this.ui.title.html(this.model.get('title'));
    },
    _remove: function(id){
      var this_ = this;
      var confirmed = confirm("Êtes vous certain de vouloir supprimer cet catégorie (les produits seront également supprimés) ?");
      if (confirmed){
        var _model = this.model;
        _model.destroy({
          success: function(model, response) {
            this_.destroy();
            AutonomieApp.router.navigate("index", {trigger: true});
            displayServerSuccess("L'élément a bien été supprimé");
            }
        });
      }
    },
    closeView: function(){
      this.ui.form.hide();
    }
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
      if (!_.isUndefined(result)){
        if (!_.isUndefined(result.id)){
          this.destroy();
          Product.router.navigate("categories/" + result.get('category_id'),
          {trigger: true});
          return;
        }
      }
      this.destroy();
      AutonomieApp.router.navigate("index", {trigger: true});
      return;
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
    }
  });

  var controller = {
    initialized:false,
    index: function(){
      this.initialize();
      App.container.empty();
      App.popup.empty();
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
      console.log("category_add");
      var model = new CategoryModel({});

      this.category_add_view = new CategoryAddFormView({
        model: model, destCollection: Product.categories
      });

      App.container.show(this.category_add_view);
    },
    category_edit: function(id){
      console.log("category_edition");
      var category = Product.categories.get(id);
      if (_.isUndefined(category)){
        Product.router.navigate('index', {trigger: true});
        return false;
      }
      this.current_category = category;
      this.main_layout = new MainLayoutView();
      App.container.show(this.main_layout);

      var category_title_view = new CategoryEditView({
        model: this.current_category, destCollection: Product.categories
      });
      this.main_layout.getRegion('title').show(category_title_view);

      this.product_collection = new ProductCollection(
         {url: category.products_url(), category_id: category.id}
      );
      var this_ = this;
      return this.product_collection.fetch(
        {
          success: function(){
            var product_list_view = new ProductListView({
              collection: this_.product_collection
            });
            this_.main_layout.getRegion('list').show(product_list_view);
          }
        }
      );
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
});
