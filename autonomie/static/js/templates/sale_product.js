(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['category_form.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<h3>\n    Catégorie :\n    <span>\n        "
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "\n    </span>\n    <div class=\"btn-group\" role=\"group\" aria-label=\"\">\n        <button\n            class='btn btn-default btn-xs edit'\n            style=\"font-size:14px;\"\n            title=\"Éditer le titre de la catégorie\">\n        <i class=\"glyphicon glyphicon-pencil\" style=\"vertical-align:middle\"> </i>\n        </button>\n        <button\n            class='btn btn-danger btn-xs remove'\n            title=\"Supprimer cette catégorie (et tous les produits qu'elle contient)\"\n            style=\"font-size:14px;\"\n            >\n            <i class=\"glyphicon glyphicon-trash danger\" style=\"vertical-align:middle\"> </i>\n        </button>\n    </div>\n</h3>\n";
},"3":function(depth0,helpers,partials,data) {
  return "    style='display:none'\n";
  },"5":function(depth0,helpers,partials,data) {
  return "        Modifier\n";
  },"7":function(depth0,helpers,partials,data) {
  return "        Ajouter\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "<form class=\"form\"\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += ">\n  <div class=\"form-group\">\n    <label class='control-label' for=\"title\">Titre de la catégorie</label>\n    <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n  </div>\n    <button type=\"submit\" class=\"btn btn-primary submit\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.program(7, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </button>\n</form>\n\n";
},"useData":true});
templates['category_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Catégories de produits\n<a class='btn btn-default' style='font-size: 14px' href='#categories/add'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<ul class='nav nav-pills nav-stacked'>\n</ul>\n";
  },"useData":true});
templates['category.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<a href='#/categories/"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "/edit' title=\"Voir cette catégorie\">"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "</a>\n";
},"useData":true});
templates['main_layout.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div id='category-title'>\n</div>\n<hr />\n<div id='product-list'>\n</div>\n<div id='group-list'>\n</div>\n";
  },"useData":true});
templates['product_empty.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<td colspan=\"4\" style=\"padding:5px\">\n    Aucun élément n'a encore été ajouté\n</td>\n";
  },"useData":true});
templates['product_form.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "                        <option value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">\n                            "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n                        </option>\n";
},"2":function(depth0,helpers,partials,data) {
  return "selected";
  },"4":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "                        <option value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">\n                            "
    + escapeExpression(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"name","hash":{},"data":data}) : helper)))
    + "\n                        </option>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<form>\n    <div class='row'>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations relatives au catalogue</legend>\n                <div class=\"form-group\">\n                    <label for='label'>Nom du produit *</label>\n                    <input class=\"form-control\" type='text' name='label' value='"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='ref'>Référence</label>\n                    <input class=\"form-control\" type='text' name='ref' value='"
    + escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ref","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n            </fieldset>\n        </div>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations utilisées lors de l'insertion dans les devis/factures</legend>\n                <div class=\"alert alert-info\">\n                    Lors de l'insertion du produit dans un devis ou une\n                    facture, les champs ci-dessous seront utilisés pour\n                    pré-remplir les données dans le document.  Ces champs sont\n                    facultatifs.\n                </div>\n                <div class=\"form-group\">\n                     <label for='description'>Description</label>\n                     <textarea id='tiny_description' name='description' class='form-control'>"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='value'>Valeur</label>\n                    <input class=\"form-control\" type='text' name='value' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='unity'>Unité</label>\n                    <select name='unity' class='form-control'>\n                    <option value=''></option>\n";
  stack1 = ((helper = (helper = helpers.unity_options || (depth0 != null ? depth0.unity_options : depth0)) != null ? helper : helperMissing),(options={"name":"unity_options","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.unity_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "                    </select>\n                </div>\n                <div class=\"form-group\">\n                    <label for='tva'>Tva</label>\n                    <select name='tva' class='form-control'>\n                    <option value=''></option>\n";
  stack1 = ((helper = (helper = helpers.tva_options || (depth0 != null ? depth0.tva_options : depth0)) != null ? helper : helperMissing),(options={"name":"tva_options","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.tva_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                    </select>\n                </div>\n            </fieldset>\n        </div>\n    </div>\n    <div class='row'>\n        <div class='col-md-6 col-md-offset-6'>\n            <div class=\"form-actions text-right\">\n                <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n                <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n            </div>\n        </div>\n    </div>\n</form>\n";
},"useData":true});
templates['product_group_form.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "                        <option value='"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + " "
    + escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ref","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(depth0,helpers,partials,data) {
  return "selected";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<form name='product_group'>\n    <div class='row'>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations relatives au catalogue</legend>\n                <div class=\"form-group\">\n                    <label for='label'>Nom de l'ouvrage *</label>\n                    <input class=\"form-control\" type='text' name='label' value='"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='ref'>Référence</label>\n                    <input class=\"form-control\" type='text' name='ref' value='"
    + escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ref","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n            </fieldset>\n        </div>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations utilisées lors de l'insertion dans les devis/factures</legend>\n                <div class='alert alert-info'>\n                    Lors de l'insertion de l'ouvrage dans un devis ou une\n                    facture, les champs ci-dessous seront utilisés pour\n                    pré-remplir les données dans le document.\n                    Ces champs sont facultatifs\n                </div>\n                <div class=\"form-group\">\n                    <label for='title'>Titre</label>\n                    <input class=\"form-control\" type='text' name='title' value='"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                     <label for='description'>Description</label>\n                     <textarea name='description' class='form-control'>"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='searches'>Produits composant cet ouvrage</label>\n                    <select multiple name='products' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.product_options || (depth0 != null ? depth0.product_options : depth0)) != null ? helper : helperMissing),(options={"name":"product_options","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.product_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                    </select>\n                </div>\n            </fieldset>\n        </div>\n    </div>\n    <div class='row'>\n        <div class='col-md-6 col-md-offset-6'>\n            <div class=\"form-actions text-right\">\n                <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n                <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n            </div>\n        </div>\n    </div>\n</form>\n";
},"useData":true});
templates['product_group_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Liste des ouvrages\n<a class='btn btn-primary add' style='font-size: 10px'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-5'>Intitulé (Réf)</th>\n        <th class='col-xs-3'>Titre</th>\n        <th class='col-xs-4 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n\n";
  },"useData":true});
templates['product_group.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "( "
    + escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ref","hash":{},"data":data}) : helper)))
    + " )";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + " ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.ref : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm edit' title=\"Modifier cet ouvrage\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <a class='btn btn-danger btn-default btn-sm remove' title='Supprimer cet ouvrage'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n</td>\n";
},"useData":true});
templates['product_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Liste des produits\n<a class='btn btn-primary add' style='font-size: 10px'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-5'>Intitulé (Réf)</th>\n        <th class='col-xs-3'>Prix Unitaire x Unité</th>\n        <th class='col-xs-1'>Tva</th>\n        <th class='col-xs-3 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n\n";
  },"useData":true});
templates['product.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "( "
    + escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ref","hash":{},"data":data}) : helper)))
    + " )";
},"3":function(depth0,helpers,partials,data) {
  return "x";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + " ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.ref : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + " ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.unity : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + " "
    + escapeExpression(((helper = (helper = helpers.unity || (depth0 != null ? depth0.unity : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"unity","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.tva_label || (depth0 != null ? depth0.tva_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva_label","hash":{},"data":data}) : helper)))
    + "</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm edit' title=\"Modifier ce produit\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <a class='btn btn-danger btn-default btn-sm remove' title='Supprimer ce produit'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n</td>\n";
},"useData":true});
})();