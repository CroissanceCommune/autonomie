(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['expenseForm.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<button class='btn btn-block btn-primary' onclick=\"$('#bookmarks').toggle();\" type='button'>Mes Favoris     >>></button>\n<div id='bookmarks' class='well' style='display:none'>\n<table class=\"table table-condensed table-stripped table-bordered\">\n";
  stack1 = ((helper = (helper = helpers.bookmark_options || (depth0 != null ? depth0.bookmark_options : depth0)) != null ? helper : helperMissing),(options={"name":"bookmark_options","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.bookmark_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</table>\n</div>\n<hr />\n<br />\n";
},"2":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<tr>\n<td>\n";
  stack1 = ((helper = (helper = helpers.attributes || (depth0 != null ? depth0.attributes : depth0)) != null ? helper : helperMissing),(options={"name":"attributes","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.attributes) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n</td>\n<td>\n<a class=\"btn btn-success edit\" data-cid='"
    + escapeExpression(((helper = (helper = helpers.cid || (depth0 != null ? depth0.cid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"cid","hash":{},"data":data}) : helper)))
    + "'>\n    <i class=\"glyphicon glyphicon-ok\"></i>\n</a>\n<a class=\"btn btn-danger delete\"  data-cid='"
    + escapeExpression(((helper = (helper = helpers.cid || (depth0 != null ? depth0.cid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"cid","hash":{},"data":data}) : helper)))
    + "'>\n    <i class=\"glyphicon glyphicon-remove-sign\"></i>\n</a>\n</td>\n</tr>\n";
},"3":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, lambda=this.lambda;
  return escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + " - HT:"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + " € - TVA:"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + " € ("
    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.type : depth0)) != null ? stack1.label : stack1), depth0))
    + ") ";
},"5":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='radio'>\n<label>\n<input type='radio' name='category' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n</label>\n</div>\n";
},"6":function(depth0,helpers,partials,data) {
  return "checked";
  },"8":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<option value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"9":function(depth0,helpers,partials,data) {
  return "selected='true'";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<form id='expenseForm' class='form ' action='#' onsubmit='return false;'>\n\n";
  stack1 = helpers.unless.call(depth0, (depth0 != null ? depth0.id : depth0), {"name":"unless","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\n<div class=\"form-group\">\n<label  for='category'>Catégorie de frais</label>\n";
  stack1 = ((helper = (helper = helpers.category_options || (depth0 != null ? depth0.category_options : depth0)) != null ? helper : helperMissing),(options={"name":"category_options","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.category_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n\n\n<div class=\"form-group\">\n<label  for='type_id'>Type de frais</label>\n<div class='controls'>\n<select class=form-control' name='type_id'>\n";
  stack1 = ((helper = (helper = helpers.type_options || (depth0 != null ? depth0.type_options : depth0)) != null ? helper : helperMissing),(options={"name":"type_options","hash":{},"fn":this.program(8, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</select>\n</div>\n</div>\n\n<div class=\"form-group\">\n<label  for='altdate'>Date</label>\n<input class=\"form-control\" name=\"altdate\" type=\"text\" autocomplete=\"off\">\n<input class=\"form-control\" name=\"date\" type=\"hidden\">\n</div>\n\n<div class=\"form-group\">\n<label  for='description'>Description</label>\n<input class=\"form-control\"type='text' name='description' value='"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "'/>\n</div>\n\n<div class=\"form-group\">\n<label  for='ht'>Montant HT</label>\n<div class=\"input-group\">\n    <input class=\"form-control\"type='text' name='ht' value='"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "' /><span class=\"input-group-addon\">&euro;</span>\n</div>\n</div>\n\n<div class=\"form-group\">\n<label  for='tva'>Montant de la Tva</label>\n<div class=\"input-group\">\n<input class=\"form-control\"type='text' name='tva' value='"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "' /><span class=\"input-group-addon\">&euro;</span>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['expenseKmForm.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='radio'>\n<label>\n<input type='radio' name='category' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n</label>\n</div>\n";
},"2":function(depth0,helpers,partials,data) {
  return "checked";
  },"4":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div  class=\"radio\">\n<label>\n<input type='radio' name='type_id' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n</label>\n</div>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<form id='expenseKmForm' class='form' action='#' onsubmit='return false;'>\n\n<div class=\"form-group\">\n<label for='category'>Catégorie de frais</label>\n";
  stack1 = ((helper = (helper = helpers.category_options || (depth0 != null ? depth0.category_options : depth0)) != null ? helper : helperMissing),(options={"name":"category_options","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.category_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n\n<div class=\"form-group\">\n<label  for='type_id'>Véhicule</label>\n";
  stack1 = ((helper = (helper = helpers.type_options || (depth0 != null ? depth0.type_options : depth0)) != null ? helper : helperMissing),(options={"name":"type_options","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n\n<div class=\"form-group\">\n<label  for='altdate'>Date</label>\n<input name=\"altdate\" class=\"form-control\" type=\"text\" autocomplete=\"off\">\n<input name=\"date\" class=\"form-control\" type=\"hidden\">\n</div>\n\n\n<div class=\"form-group\">\n<label  for='start'>Point de départ</label>\n<input type='text' class='form-control' name='start' value='"
    + escapeExpression(((helper = (helper = helpers.start || (depth0 != null ? depth0.start : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start","hash":{},"data":data}) : helper)))
    + "'/>\n</div>\n\n<div class=\"form-group\">\n<label  for='end'>Point d'arrivée</label>\n<input type='text' class='form-control' name='end' value='"
    + escapeExpression(((helper = (helper = helpers.end || (depth0 != null ? depth0.end : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end","hash":{},"data":data}) : helper)))
    + "'/>\n</div>\n\n<div class=\"form-group\">\n<label  for='ht'>Nombre de Kilomètres</label>\n<div class=\"input-group\">\n    <input type='text' class='form-control' name='km' value='"
    + escapeExpression(((helper = (helper = helpers.km || (depth0 != null ? depth0.km : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"km","hash":{},"data":data}) : helper)))
    + "' /><span class=\"input-group-addon\">Km</span>\n</div>\n</div>\n\n<div class='form-group'>\n<label  for='description'>Description</label>\n<input type='text' class='form-control' name='description' value='"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "' />\n<span class=\"help-block\"> Le cas échéant, indiquer la prestation liée à ces frais</span>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['expenseKmList.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "            <div>\n                <a href=\"#kmlines/add/1\" class='btn btn-info visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "            <th class=\"hidden-print\">Actions</th>\n";
  },"5":function(depth0,helpers,partials,data) {
  return "                <td class=\"hidden-print\"></td>\n";
  },"7":function(depth0,helpers,partials,data) {
  return "            <div>\n                <a href=\"#kmlines/add/2\" class='btn btn-info visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div>\n    <div class=\"row\">\n        <div class=\"col-xs-4\">\n            <h3 style=\"margin-top:0px\">\n                Dépenses kilométriques : Frais\n            </h3>\n            <span class=\"help-block\">\n                Dépenses liées au fonctionnement de l'entreprise\n            </span>\n        </div>\n        <div class=\"col-xs-8\">\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </div>\n    </div>\n\n    <table class=\"opa table table-striped table-bordered table-condensed\">\n        <thead>\n            <th>Date</th>\n            <th>Type</th>\n            <th>Prestation</th>\n            <th>Point de départ</th>\n            <th>Point d'arrivée</th>\n            <th>Kms</th>\n            <th>Indemnités</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody class='internal'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='6'>Total</td>\n                <td id='km_internal_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </tr>\n        </tfoot>\n    </table>\n    <br/>\n    <div class=\"row\">\n        <div class=\"col-xs-4\">\n            <h3 style=\"margin-top:0px\">\n                Dépenses kilométriques : Achats\n            </h3>\n            <span class=\"help-block\">\n                Dépenses concernant directement votre activité auprès de vos clients\n            </span>\n        </div>\n        <div class=\"col-xs-8\">\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </div>\n    </div>\n    <table class=\"opa table table-striped table-bordered table-condensed\">\n        <thead>\n            <th>Date</th>\n            <th>Type</th>\n            <th>Prestation</th>\n            <th>Point de départ</th>\n            <th>Point d'arrivée</th>\n            <th>Kms</th>\n            <th>Indemnités</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody class='activity'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='6'>Total</td>\n                <td id='km_activity_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            </tr>\n        </tfoot>\n    </table>\n</div>\n";
},"useData":true});
templates['expenseKm.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td class=\"hidden-print\"><a class='btn btn-default' href='"
    + escapeExpression(((helper = (helper = helpers.edit_url || (depth0 != null ? depth0.edit_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"edit_url","hash":{},"data":data}) : helper)))
    + "' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>\n<a class='btn btn-default remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</td>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.altdate || (depth0 != null ? depth0.altdate : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"altdate","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.start || (depth0 != null ? depth0.start : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.end || (depth0 != null ? depth0.end : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.km || (depth0 != null ? depth0.km : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"km","hash":{},"data":data}) : helper)))
    + "</td>\n<td>";
  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  buffer += "</td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
templates['expenseList.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "            <div>\n            <a href=\"#lines/add/1\" class='btn btn-info' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            <a href=\"#tel/add\" class='btn btn-info' title=\"Ajouter une lignei de frais téléphonique\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais téléphoniques</a>\n            </div>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "            <th class=\"hidden-print\">Actions</th>\n";
  },"5":function(depth0,helpers,partials,data) {
  return "                <td class=\"hidden-print\"></td>\n";
  },"7":function(depth0,helpers,partials,data) {
  return "            <div>\n                <a href=\"#lines/add/2\" class='btn btn-info' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div>\n    <div class=\"row\">\n        <div class=\"col-xs-4\">\n            <h3 style=\"margin-top:0px\">\n                Frais\n            </h3>\n            <span class=\"help-block\">\n                Dépenses liées au fonctionnement de l'entreprise\n            </span>\n        </div>\n        <div class=\"col-xs-8\">\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </div>\n    </div>\n    <table class=\"opa table table-bordered table-condensed\">\n        <thead>\n            <th>Date</th>\n            <th>Type de frais</th>\n            <th>Description</th>\n            <th>Montant HT</th>\n            <th>Tva</th>\n            <th>Total</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody class='internal'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='5'>Total</td>\n                <td id='internal_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </tr>\n        </tfoot>\n    </table>\n    <br />\n    <div class=\"row\">\n        <div class=\"col-xs-4\">\n            <h3 style=\"margin-top:0px\">\n                Achats\n            </h3>\n            <span class=\"help-block\">\n                Dépenses concernant directement votre activité auprès de vos clients\n            </span>\n        </div>\n        <div class=\"col-xs-8\">\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </div>\n    </div>\n    <table class=\"opa table table-bordered table-condensed\">\n        <thead>\n            <th>Date</th>\n            <th>Type de frais</th>\n            <th>Description</th>\n            <th>Montant HT</th>\n            <th>Tva</th>\n            <th>Total</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody class='activity'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='5'>Total</td>\n                <td id='activity_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            </tr>\n        </tfoot>\n    </table>\n</div>\n";
},"useData":true});
templates['expense.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td class='hidden-print'><a class='btn btn-default' href='"
    + escapeExpression(((helper = (helper = helpers.edit_url || (depth0 != null ? depth0.edit_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"edit_url","hash":{},"data":data}) : helper)))
    + "' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>\n<a class='btn btn-default remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a>\n<a class='btn btn-default' href='"
    + escapeExpression(((helper = (helper = helpers.bookmark_url || (depth0 != null ? depth0.bookmark_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"bookmark_url","hash":{},"data":data}) : helper)))
    + "'><i class='icon-star-empty'></i>&nbsp;Favoris</a>\n</td>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.altdate || (depth0 != null ? depth0.altdate : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"altdate","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "</td>\n<td>";
  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  buffer += "</td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
templates['expenseorphan.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.altdate || (depth0 != null ? depth0.altdate : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"altdate","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
    + "(ce type ne semble plus exister)</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "</td>\n<td>";
  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</td>\n<td class=\"hidden-print\"></td>\n";
},"useData":true});
templates['expenseTelForm.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<option value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(depth0,helpers,partials,data) {
  return "selected='true'";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<form id='expenseTelForm' class='form ' action='#' onsubmit='return false;'>\n\n<div class=\"form-group\">\n<label class=\"control-label\" for='type_id'>Type de frais</label>\n<div class='controls'>\n<select class='input-xlarge' name='type_id'>\n";
  stack1 = ((helper = (helper = helpers.type_options || (depth0 != null ? depth0.type_options : depth0)) != null ? helper : helperMissing),(options={"name":"type_options","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</select>\n</div>\n</div>\n\n<div class=\"form-group\">\n<label class=\"control-label\" for='ht'>Montant HT</label>\n<div class='controls'>\n<div class=\"input-group\">\n    <input type='text' class='input-small' name='ht' value='"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "' /><span class=\"input-group-addon\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"form-group\">\n<label class=\"control-label\" for='tva'>Montant de la Tva</label>\n<div class='controls'>\n<div class=\"input-group\">\n<input type='text' class='input-small' name='tva' value='"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "' /><span class=\"input-group-addon\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn btn-default\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['expensetel.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<td><div class='form-group'><div class='controls'><input type='text' class='input-small' value='"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "' name='ht'/></div></div></td>\n<td><div class='form-group'><div class='controls'><input type='text' class='input-small' value='"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "' name='tva'/></div></div></td>\n<td><span class='total'>";
  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</span></td>\n<td class=\"hidden-print\">\n<a class='btn btn-default remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a>\n</td>\n";
},"3":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "</td>\n<td>";
  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</td>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td colspan='3'>"
    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
    + "</td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.noop,"inverse":this.program(3, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
})();