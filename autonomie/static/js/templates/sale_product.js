(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['category.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<a href='#/categories/"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "/edit' title=\"Voir cette catégorie\">"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "</a>\n";
},"useData":true});
templates['category_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper;

  return "<h3>\n    Catégorie :\n    <span>\n        "
    + container.escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"title","hash":{},"data":data}) : helper)))
    + "\n    </span>\n    <div class=\"btn-group\" role=\"group\" aria-label=\"\">\n        <button\n            class='btn btn-default btn-xs edit'\n            style=\"font-size:14px;\"\n            title=\"Éditer le titre de la catégorie\">\n        <i class=\"glyphicon glyphicon-pencil\" style=\"vertical-align:middle\"> </i>\n        </button>\n        <button\n            class='btn btn-danger btn-xs remove'\n            title=\"Supprimer cette catégorie (et tous les produits qu'elle contient)\"\n            style=\"font-size:14px;\"\n            >\n            <i class=\"glyphicon glyphicon-trash danger\" style=\"vertical-align:middle\"> </i>\n        </button>\n    </div>\n</h3>\n";
},"3":function(container,depth0,helpers,partials,data) {
    return "    style='display:none'\n";
},"5":function(container,depth0,helpers,partials,data) {
    return "        Modifier\n";
},"7":function(container,depth0,helpers,partials,data) {
    return "        Ajouter\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {});

  return ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.title : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "<form class=\"form\"\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.title : depth0),{"name":"if","hash":{},"fn":container.program(3, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + ">\n  <div class=\"form-group\">\n    <label class='control-label' for=\"title\">Titre de la catégorie</label>\n    <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + container.escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n  </div>\n    <button type=\"submit\" class=\"btn btn-primary submit\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.title : depth0),{"name":"if","hash":{},"fn":container.program(5, data, 0),"inverse":container.program(7, data, 0),"data":data})) != null ? stack1 : "")
    + "    </button>\n</form>\n\n";
},"useData":true});
templates['category_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Catégories de produits\n<a class='btn btn-default' style='font-size: 14px' href='#categories/add'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<ul class='nav nav-pills nav-stacked'>\n</ul>\n";
},"useData":true});
templates['main_layout.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<div id='category-title'>\n</div>\n<hr />\n<div id='product-list'>\n</div>\n<div id='group-list'>\n</div>\n<div id='training-group-list'>\n</div>\n";
},"useData":true});
templates['product.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper;

  return "( "
    + container.escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"ref","hash":{},"data":data}) : helper)))
    + " )";
},"3":function(container,depth0,helpers,partials,data) {
    return "x";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<td>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + " "
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.ref : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "</td>\n<td>"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + " "
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.unity : depth0),{"name":"if","hash":{},"fn":container.program(3, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + " "
    + alias4(((helper = (helper = helpers.unity || (depth0 != null ? depth0.unity : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"unity","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + alias4(((helper = (helper = helpers.tva_label || (depth0 != null ? depth0.tva_label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"tva_label","hash":{},"data":data}) : helper)))
    + "</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm edit' title=\"Modifier ce produit\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <a class='btn btn-danger btn-default btn-sm remove' title='Supprimer ce produit'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n</td>\n";
},"useData":true});
templates['product_empty.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<td colspan=\"4\" style=\"padding:5px\">\n    Aucun élément n'a encore été ajouté\n</td>\n";
},"useData":true});
templates['product_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                        <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">\n                            "
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "\n                        </option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"4":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                        <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">\n                            "
    + alias4(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"name","hash":{},"data":data}) : helper)))
    + "\n                        </option>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, alias5=helpers.blockHelperMissing, buffer = 
  "<form>\n    <div class='row'>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations relatives au catalogue</legend>\n                <div class=\"form-group\">\n                    <label for='label'>Nom du produit *</label>\n                    <input class=\"form-control\" type='text' name='label' value='"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='ref'>Référence</label>\n                    <input class=\"form-control\" type='text' name='ref' value='"
    + alias4(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"ref","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n            </fieldset>\n        </div>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations utilisées lors de l'insertion dans les devis/factures</legend>\n                <div class=\"alert alert-info\">\n                    Lors de l'insertion du produit dans un devis ou une\n                    facture, les champs ci-dessous seront utilisés pour\n                    pré-remplir les données dans le document.  Ces champs sont\n                    facultatifs.\n                </div>\n                <div class=\"form-group\">\n                     <label for='description'>Description</label>\n                     <textarea id='tiny_description' name='description' class='form-control'>"
    + alias4(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='value'>Valeur</label>\n                    <input class=\"form-control\" type='text' name='value' value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' pattern=\"[0-9]+([\\.,][0-9]+)?\"/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='unity'>Unité</label>\n                    <select name='unity' class='form-control'>\n                    <option value=''></option>\n";
  stack1 = ((helper = (helper = helpers.unity_options || (depth0 != null ? depth0.unity_options : depth0)) != null ? helper : alias2),(options={"name":"unity_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.unity_options) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "                    </select>\n                </div>\n                <div class=\"form-group\">\n                    <label for='tva'>Tva</label>\n                    <select name='tva' class='form-control'>\n                    <option value=''></option>\n";
  stack1 = ((helper = (helper = helpers.tva_options || (depth0 != null ? depth0.tva_options : depth0)) != null ? helper : alias2),(options={"name":"tva_options","hash":{},"fn":container.program(4, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.tva_options) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                    </select>\n                </div>\n            </fieldset>\n        </div>\n    </div>\n    <div class='row'>\n        <div class='col-md-6 col-md-offset-6'>\n            <div class=\"form-actions text-right\">\n                <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n                <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n            </div>\n        </div>\n    </div>\n</form>\n";
},"useData":true});
templates['product_group.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper;

  return "( "
    + container.escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"ref","hash":{},"data":data}) : helper)))
    + " )";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<td>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + " "
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.ref : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "</td>\n<td>"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm edit' title=\"Modifier cet ouvrage\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <a class='btn btn-danger btn-default btn-sm remove' title='Supprimer cet ouvrage'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n</td>\n";
},"useData":true});
templates['product_group_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                        <option value='"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + " "
    + alias4(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"ref","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<form name='product_group'>\n    <div class='row'>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations relatives au catalogue</legend>\n                <div class=\"form-group\">\n                    <label for='label'>Nom de l'ouvrage *</label>\n                    <input class=\"form-control\" type='text' name='label' value='"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='ref'>Référence</label>\n                    <input class=\"form-control\" type='text' name='ref' value='"
    + alias4(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"ref","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n            </fieldset>\n        </div>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations utilisées lors de l'insertion dans les devis/factures</legend>\n                <div class='alert alert-info'>\n                    Lors de l'insertion de l'ouvrage dans un devis ou une\n                    facture, les champs ci-dessous seront utilisés pour\n                    pré-remplir les données dans le document.\n                    Ces champs sont facultatifs\n                </div>\n                <div class=\"form-group\">\n                    <label for='title'>Titre</label>\n                    <input class=\"form-control\" type='text' name='title' value='"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                     <label for='description'>Description</label>\n                     <textarea name='description' class='form-control'>"
    + alias4(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='searches'>Produits composant cet ouvrage</label>\n                    <select multiple name='products' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.product_options || (depth0 != null ? depth0.product_options : depth0)) != null ? helper : alias2),(options={"name":"product_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.product_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                    </select>\n                </div>\n            </fieldset>\n        </div>\n    </div>\n    <div class='row'>\n        <div class='col-md-6 col-md-offset-6'>\n            <div class=\"form-actions text-right\">\n                <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n                <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n            </div>\n        </div>\n    </div>\n</form>\n";
},"useData":true});
templates['product_group_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Liste des ouvrages\n<a class='btn btn-primary add' style='font-size: 10px'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-5'>Intitulé (Réf)</th>\n        <th class='col-xs-3'>Titre</th>\n        <th class='col-xs-4 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n\n";
},"useData":true});
templates['product_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Liste des produits\n<a class='btn btn-primary add' style='font-size: 10px'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-5'>Intitulé (Réf)</th>\n        <th class='col-xs-3'>Prix Unitaire x Unité</th>\n        <th class='col-xs-1'>Tva</th>\n        <th class='col-xs-3 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n\n";
},"useData":true});
templates['training_group.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper;

  return "( "
    + container.escapeExpression(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"ref","hash":{},"data":data}) : helper)))
    + " )";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<td>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + " "
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.ref : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "</td>\n<td>"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm edit' title=\"Modifier cette formation\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <a class='btn btn-danger btn-default btn-sm remove' title='Supprimer cet formation'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n\n</td>";
},"useData":true});
templates['training_group_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                        <option value='"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"4":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                        <option value='"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + " "
    + alias4(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"ref","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, alias5=helpers.blockHelperMissing, buffer = 
  "<form name='training_group'>\n    <div class='row'>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations relatives au catalogue</legend>\n                <div class=\"form-group\">\n                    <label for='label'>Intitulé de la formation*</label>\n                    <input class=\"form-control\" type='text' name='label' value='"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='ref'>Référence</label>\n                    <input class=\"form-control\" type='text' name='ref' value='"
    + alias4(((helper = (helper = helpers.ref || (depth0 != null ? depth0.ref : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"ref","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                     <label for='goals'>Objectifs à atteindre à l'issue de la formation</label>\n                     <div class='alert alert-info'>\n                         Les objectifs doivent être obligatoirement décrit\n                         avec des verbes d'actions\n                     </div>\n                     <textarea name='goals' class='form-control'>"
    + alias4(((helper = (helper = helpers.goals || (depth0 != null ? depth0.goals : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"goals","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='prerequisites'>Pré-requis obligatoire de la formation</label>\n                     <textarea name='prerequisites' class='form-control'>"
    + alias4(((helper = (helper = helpers.prerequisites || (depth0 != null ? depth0.prerequisites : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"prerequisites","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='for_who'>Pour qui?</label>\n                    <div class='alert alert-info'>\n                        Public susceptible de participer à cette formation\n                    </div>\n                     <textarea name='for_who' class='form-control'>"
    + alias4(((helper = (helper = helpers.for_who || (depth0 != null ? depth0.for_who : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"for_who","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='duration'>Durée en heures et en jour(s) pour la formation</label>\n                    <div class='alert alert-info'>\n                        Durée obligatoire minimale 7 heures soit 1 jour\n                    </div>\n                    <input class=\"form-control\" type='text' name='duration' value='"
    + alias4(((helper = (helper = helpers.duration || (depth0 != null ? depth0.duration : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"duration","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                     <label for='content'>Contenu détaillé de la formation</label>\n                    <div class='alert alert-info'>\n                        Trame par étapes\n                    </div>\n                     <textarea name='content' class='form-control'>"
    + alias4(((helper = (helper = helpers.content || (depth0 != null ? depth0.content : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"content","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='teaching_method'>Les moyens pédagogiques utilisés</label>\n                     <textarea name='teaching_method' class='form-control'>"
    + alias4(((helper = (helper = helpers.teaching_method || (depth0 != null ? depth0.teaching_method : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"teaching_method","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='logistics_means'>Les moyens logistiques à disposition</label>\n                     <textarea name='logistics_means' class='form-control'>"
    + alias4(((helper = (helper = helpers.logistics_means || (depth0 != null ? depth0.logistics_means : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"logistics_means","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='more_stuff'>Quels sont les plus de cette formation ?</label>\n                     <textarea name='more_stuff' class='form-control'>"
    + alias4(((helper = (helper = helpers.more_stuff || (depth0 != null ? depth0.more_stuff : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"more_stuff","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='evaluation'>Modalités d'évaluation de la formation</label>\n                    <div class='alert alert-info'>\n                        Par exemple : questionnaire d'évaluation, exercices-tests, questionnaire\n                        de satisfaction, évaluation formative.\n                    </div>\n                     <textarea name='evaluation' class='form-control'>"
    + alias4(((helper = (helper = helpers.evaluation || (depth0 != null ? depth0.evaluation : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"evaluation","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='place'>Lieu de la formation</label>\n                    <div class='alert alert-info'>\n                        Villes, zones géographiques où la formation peut être mise en place\n                    </div>\n                     <textarea name='place' class='form-control'>"
    + alias4(((helper = (helper = helpers.place || (depth0 != null ? depth0.place : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"place","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='modality'>Modalité de formation</label>\n                    <select multiple name='modality' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.modality_options || (depth0 != null ? depth0.modality_options : depth0)) != null ? helper : alias2),(options={"name":"modality_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.modality_options) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "                    </select>\n                </div>\n                <div class=\"form-group\">\n                     <label for='type'>Type de formation</label>\n                     <textarea name='type' class='form-control'>"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='date'>Dates de la formation</label>\n                    <input class=\"form-control\" type='text' name='date' value='"
    + alias4(((helper = (helper = helpers.date || (depth0 != null ? depth0.date : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"date","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                    <label for='price'>Dates de la formation</label>\n                    <input class=\"form-control\" type='text' name='price' value='"
    + alias4(((helper = (helper = helpers.price || (depth0 != null ? depth0.price : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"price","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                     <label for='free_1'>Champ libre 1</label>\n                     <textarea name='free_1' class='form-control'>"
    + alias4(((helper = (helper = helpers.free_1 || (depth0 != null ? depth0.free_1 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"free_1","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='free_2'>Champ libre 2</label>\n                     <textarea name='free_2' class='form-control'>"
    + alias4(((helper = (helper = helpers.free_2 || (depth0 != null ? depth0.free_2 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"free_2","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                     <label for='free_3'>Champ libre 3</label>\n                     <textarea name='free_3' class='form-control'>"
    + alias4(((helper = (helper = helpers.free_3 || (depth0 != null ? depth0.free_3 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"free_3","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n            </fieldset>\n        </div>\n        <div class='col-md-6'>\n            <fieldset>\n                <legend>Informations utilisées lors de l'insertion dans les devis/factures</legend>\n                <div class='alert alert-info'>\n                    Lors de l'insertion de l'ouvrage dans un devis ou une\n                    facture, les champs ci-dessous seront utilisés pour\n                    pré-remplir les données dans le document.\n                    Ces champs sont facultatifs\n                </div>\n                <div class=\"form-group\">\n                    <label for='title'>Titre</label>\n                    <input class=\"form-control\" type='text' name='title' value='"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "'/>\n                </div>\n                <div class=\"form-group\">\n                     <label for='description'>Description</label>\n                     <textarea name='description' class='form-control'>"
    + alias4(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                <div class=\"form-group\">\n                    <label for='searches'>Produits composant cet ouvrage</label>\n                    <select multiple name='products' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.product_options || (depth0 != null ? depth0.product_options : depth0)) != null ? helper : alias2),(options={"name":"product_options","hash":{},"fn":container.program(4, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.product_options) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                    </select>\n                </div>\n            </fieldset>\n        </div>\n    </div>\n    <div class='row'>\n        <div class='col-md-6 col-md-offset-6'>\n            <div class=\"form-actions text-right\">\n                <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n                <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n            </div>\n        </div>\n    </div>\n</form>\n";
},"useData":true});
templates['training_group_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Liste des formations\n<a class='btn btn-primary add' style='font-size: 10px'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-5'>Intitulé (Réf)</th>\n        <th class='col-xs-3'>Titre</th>\n        <th class='col-xs-4 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>";
},"useData":true});
})();