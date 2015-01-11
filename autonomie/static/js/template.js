(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['holidayForm.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<form id='holidayForm' class='form' action='#' onsubmit='return false;'>\n<div class=\"control-group\">\n<label class=\"control-label\" for='alt_start_date'>Début</label>\n<div class='controls'>\n    <input name=\"alt_start_date\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n    <input name=\"start_date\" type=\"hidden\">\n</div>\n</div>\n<div class=\"control-group\">\n<label class=\"control-label\" for='alt_end_date'>Fin</label>\n<div class='controls'>\n    <input name=\"alt_end_date\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n    <input name=\"end_date\" type=\"hidden\">\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
  },"useData":true});
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
  return buffer + "\n</td>\n<td>\n<a class=\"btn btn-mini edit\" data-cid='"
    + escapeExpression(((helper = (helper = helpers.cid || (depth0 != null ? depth0.cid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"cid","hash":{},"data":data}) : helper)))
    + "'>\n    <i class=\"icon-ok\"></i>\n</a>\n<a class=\"btn btn-mini delete\"  data-cid='"
    + escapeExpression(((helper = (helper = helpers.cid || (depth0 != null ? depth0.cid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"cid","hash":{},"data":data}) : helper)))
    + "'>\n    <i class=\"icon-remove-sign\"></i>\n</a>\n</td>\n</tr>\n";
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
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<label class=\"radio\">\n<input type='radio' name='category' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n</label>\n";
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
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<form id='expenseForm' class='form form-horizontal' action='#' onsubmit='return false;'>\n\n";
  stack1 = helpers.unless.call(depth0, (depth0 != null ? depth0.id : depth0), {"name":"unless","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\n<div class=\"control-group\">\n<label class=\"control-label\" for='category'>Catégorie de frais</label>\n<div class='controls'>\n";
  stack1 = ((helper = (helper = helpers.category_options || (depth0 != null ? depth0.category_options : depth0)) != null ? helper : helperMissing),(options={"name":"category_options","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.category_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n</div>\n\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='type_id'>Type de frais</label>\n<div class='controls'>\n<select class='input-xxlarge' name='type_id'>\n";
  stack1 = ((helper = (helper = helpers.type_options || (depth0 != null ? depth0.type_options : depth0)) != null ? helper : helperMissing),(options={"name":"type_options","hash":{},"fn":this.program(8, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</select>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='altdate'>Date</label>\n<div class='controls'>\n<input name=\"altdate\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n<input name=\"date\" class=\"input-small\" type=\"hidden\">\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='description'>Description</label>\n<div class='controls'>\n<input type='text' class='input-xxlarge' name='description' value='"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='ht'>Montant HT</label>\n<div class='controls'>\n<div class=\"input-append\">\n    <input type='text' class='input-small' name='ht' value='"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='tva'>Montant de la Tva</label>\n<div class='controls'>\n<div class=\"input-append\">\n<input type='text' class='input-small' name='tva' value='"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['expensetel.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<td><div class='control-group'><div class='controls'><input type='text' class='input-small' value='"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "' name='ht'/></div></div></td>\n<td><div class='control-group'><div class='controls'><input type='text' class='input-small' value='"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "' name='tva'/></div></div></td>\n<td><span class='total'>";
  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</span></td>\n<td class=\"hidden-print\">\n<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a>\n</td>\n";
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
templates['expenseList.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "    <div class=\"inline-element\">\n    <a href=\"#lines/add/1\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n    <a href=\"#tel/add\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une lignei de frais téléphonique\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais téléphoniques</a>\n    </div>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "        <th class=\"hidden-print\">Actions</th>\n";
  },"5":function(depth0,helpers,partials,data) {
  return "            <td class=\"hidden-print\"></td>\n";
  },"7":function(depth0,helpers,partials,data) {
  return "    <div class=\"inline-element\">\n    <a href=\"#lines/add/2\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n    </div>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div>\n<table class=\"opa table table-bordered table-condensed\">\n    <caption>\n    Frais liés au fonctionnement de l'entreprise\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </caption>\n    <thead>\n        <th>Date</th>\n        <th>Type de frais</th>\n        <th>Description</th>\n        <th>Montant HT</th>\n        <th>Tva</th>\n        <th>Total</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </thead>\n    <tbody class='internal'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='5'>Total</td>\n            <td id='internal_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </tr>\n    </tfoot>\n</table>\n<br />\n<table class=\"opa table table-bordered table-condensed\">\n    <caption>\n    Frais concernant directement votre activité auprès de vos clients\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </caption>\n    <thead>\n        <th>Date</th>\n        <th>Type de frais</th>\n        <th>Description</th>\n        <th>Montant HT</th>\n        <th>Tva</th>\n        <th>Total</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </thead>\n    <tbody class='activity'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='5'>Total</td>\n            <td id='activity_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        </tr>\n    </tfoot>\n</table>\n</div>\n";
},"useData":true});
templates['serverMessage.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "class=\"alert alert-error\">\n<i class=\"icon-warning-sign\"></i>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "class=\"alert alert-success\">\n<i class=\"icon-ok\"></i>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<div\n";
  stack1 = ((helper = (helper = helpers.error || (depth0 != null ? depth0.error : depth0)) != null ? helper : helperMissing),(options={"name":"error","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.error) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  stack1 = ((helper = (helper = helpers.error || (depth0 != null ? depth0.error : depth0)) != null ? helper : helperMissing),(options={"name":"error","hash":{},"fn":this.noop,"inverse":this.program(3, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.error) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "<button class=\"close\" data-dismiss=\"alert\" type=\"button\">×</button>\n"
    + escapeExpression(((helper = (helper = helpers.msg || (depth0 != null ? depth0.msg : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"msg","hash":{},"data":data}) : helper)))
    + "\n</div>\n";
},"useData":true});
templates['expense.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td class='hidden-print'><a class='btn' href='"
    + escapeExpression(((helper = (helper = helpers.edit_url || (depth0 != null ? depth0.edit_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"edit_url","hash":{},"data":data}) : helper)))
    + "' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>\n<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a>\n<a class='btn' href='"
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
templates['csv_import_job.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "<div class=\"well text-center btn-warning\">\n<i class=\"fa fa-cog fa-spin fa-4x\"></i>\n<br />\n<b>L'import est en cours</b>\n</div>\n";
  },"3":function(depth0,helpers,partials,data) {
  var stack1, buffer = "\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.failed : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"4":function(depth0,helpers,partials,data) {
  return "<div class=\"well text-center btn-danger\">\n<i class=\"fa fa-warning fa-4x\"></i>\n<br />\n<b>L'import a échoué</b>\n</div>\n";
  },"6":function(depth0,helpers,partials,data) {
  return "\n<div class=\"well text-center btn-success\">\n<i class=\"fa fa-check fa-4x\"></i>\n<br />\n<b>L'import s'est déroulé avec succès</b>\n</div>\n\n";
  },"8":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row-fluid'>\n<div class='span6'>\n<h4>Messages</h4>\n"
    + escapeExpression(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_message || (depth0 != null ? depth0.has_message : depth0)) != null ? helper : helperMissing),(options={"name":"has_message","hash":{},"fn":this.noop,"inverse":this.program(9, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_message) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "<h4>Erreurs</h4>\n"
    + escapeExpression(((helper = (helper = helpers.err_message || (depth0 != null ? depth0.err_message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"err_message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_err_message || (depth0 != null ? depth0.has_err_message : depth0)) != null ? helper : helperMissing),(options={"name":"has_err_message","hash":{},"fn":this.noop,"inverse":this.program(11, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_err_message) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n<div class='span6'>\n<h4>Télécharger des données</h4>\n";
  stack1 = ((helper = (helper = helpers.has_unhandled_datas || (depth0 != null ? depth0.has_unhandled_datas : depth0)) != null ? helper : helperMissing),(options={"name":"has_unhandled_datas","hash":{},"fn":this.program(13, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_unhandled_datas) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "<hr>\n";
  stack1 = ((helper = (helper = helpers.has_errors || (depth0 != null ? depth0.has_errors : depth0)) != null ? helper : helperMissing),(options={"name":"has_errors","hash":{},"fn":this.program(15, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_errors) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n</div>\n";
},"9":function(depth0,helpers,partials,data) {
  return "Aucun message n'é été retourné\n";
  },"11":function(depth0,helpers,partials,data) {
  return "Aucune erreur n'a été retournée\n";
  },"13":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "Télécharger les données du fichier qui n'ont pas été importées :\n<a class='btn btn-warning' href=\""
    + escapeExpression(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"url","hash":{},"data":data}) : helper)))
    + "?action=unhandled.csv\">Télécharger</a>\n";
},"15":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "Télécharger les lignes du fichier contenant des erreurs :\n<a class='btn btn-danger' href=\""
    + escapeExpression(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"url","hash":{},"data":data}) : helper)))
    + "?action=errors.csv\">Télécharger</a>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row-fluid'>\n<div class='span6'>\n<h2>Import de données</h2>\n<ul>\n<li>Identifiant de la tâche : "
    + escapeExpression(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Initialisée le : "
    + escapeExpression(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Mise à jour le : "
    + escapeExpression(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n</ul>\n</div>\n<div class=\"span3 offset3\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.running : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n</div>\n<hr />\n";
  stack1 = ((helper = (helper = helpers.running || (depth0 != null ? depth0.running : depth0)) != null ? helper : helperMissing),(options={"name":"running","hash":{},"fn":this.noop,"inverse":this.program(8, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.running) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
templates['holiday.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td>"
    + escapeExpression(((helper = (helper = helpers.alt_start_date || (depth0 != null ? depth0.alt_start_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"alt_start_date","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.alt_end_date || (depth0 != null ? depth0.alt_end_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"alt_end_date","hash":{},"data":data}) : helper)))
    + "</td>\n<td><a class='btn edit'><i class='icon icon-pencil'></i>&nbsp;Éditer</a><a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a></td>\n";
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
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<form id='expenseTelForm' class='form form-horizontal' action='#' onsubmit='return false;'>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='type_id'>Type de frais</label>\n<div class='controls'>\n<select class='input-xlarge' name='type_id'>\n";
  stack1 = ((helper = (helper = helpers.type_options || (depth0 != null ? depth0.type_options : depth0)) != null ? helper : helperMissing),(options={"name":"type_options","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</select>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='ht'>Montant HT</label>\n<div class='controls'>\n<div class=\"input-append\">\n    <input type='text' class='input-small' name='ht' value='"
    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='tva'>Montant de la Tva</label>\n<div class='controls'>\n<div class=\"input-append\">\n<input type='text' class='input-small' name='tva' value='"
    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['holidayList.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div>\n    <table class=\"opa table table-bordered table-condensed\">\n        <caption>\n        Vos congés\n            <div class=\"inline-element\">\n                <a class='btn add' title=\"Déclarer un congés\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n        </caption>\n        <thead>\n            <th>Date de début</th>\n            <th>Date de fin</th>\n            <th>Actions</th>\n        </thead>\n        <tbody>\n        </tbody>\n    </table>\n</div>\n";
  },"useData":true});
templates['expenseKm.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td class=\"hidden-print\"><a class='btn' href='"
    + escapeExpression(((helper = (helper = helpers.edit_url || (depth0 != null ? depth0.edit_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"edit_url","hash":{},"data":data}) : helper)))
    + "' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>\n<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</td>\n";
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
templates['expenseKmForm.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<label class=\"radio\">\n<input type='radio' name='category' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n</label>\n";
},"2":function(depth0,helpers,partials,data) {
  return "checked";
  },"4":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<label class=\"radio\">\n<input type='radio' name='type_id' value='"
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : helperMissing),(options={"name":"selected","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "> "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "\n</label>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "<form id='expenseKmForm' class='form' action='#' onsubmit='return false;'>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='category'>Catégorie de frais</label>\n<div class='controls'>\n";
  stack1 = ((helper = (helper = helpers.category_options || (depth0 != null ? depth0.category_options : depth0)) != null ? helper : helperMissing),(options={"name":"category_options","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.category_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='type_id'>Véhicule</label>\n<div class='controls'>\n";
  stack1 = ((helper = (helper = helpers.type_options || (depth0 != null ? depth0.type_options : depth0)) != null ? helper : helperMissing),(options={"name":"type_options","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='altdate'>Date</label>\n<div class='controls'>\n<input name=\"altdate\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n<input name=\"date\" class=\"input-small\" type=\"hidden\">\n</div>\n</div>\n\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='start'>Point de départ</label>\n<div class='controls'>\n<input type='text' class='input-medium' name='start' value='"
    + escapeExpression(((helper = (helper = helpers.start || (depth0 != null ? depth0.start : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start","hash":{},"data":data}) : helper)))
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='end'>Point d'arrivée</label>\n<div class='controls'>\n<input type='text' class='input-medium' name='end' value='"
    + escapeExpression(((helper = (helper = helpers.end || (depth0 != null ? depth0.end : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end","hash":{},"data":data}) : helper)))
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='ht'>Nombre de Kilomètres</label>\n<div class='controls'>\n<div class=\"input-append\">\n    <input type='text' class='input-small' name='km' value='"
    + escapeExpression(((helper = (helper = helpers.km || (depth0 != null ? depth0.km : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"km","hash":{},"data":data}) : helper)))
    + "' /><span class=\"add-on\">km</span>\n</div>\n</div>\n</div>\n\n<div class='control-group'>\n<label class=\"control-label\" for='description'>Description</label>\n<div class='controls'>\n<input type='text' class='input-xlarge' name='description' value='"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "' />\n<span class=\"help-block\"> Le cas échéant, indiquer la prestation liée à ces frais</span>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['expenseKmList.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "            <div class=\"inline-element\">\n<a href=\"#kmlines/add/1\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n";
  },"3":function(depth0,helpers,partials,data) {
  return "            <th class=\"hidden-print\">Actions</th>\n";
  },"5":function(depth0,helpers,partials,data) {
  return "                <td class=\"hidden-print\"></td>\n";
  },"7":function(depth0,helpers,partials,data) {
  return "            <div class=\"inline-element\">\n<a href=\"#kmlines/add/2\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div>\n\n    <table class=\"opa table table-striped table-bordered table-condensed\">\n        <caption>\n        Frais kilométriques liés au fonctionnement de l'entreprise\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </caption>\n        <thead>\n            <th>Date</th>\n            <th>Type</th>\n            <th>Prestation</th>\n            <th>Point de départ</th>\n            <th>Point d'arrivée</th>\n            <th>Kms</th>\n            <th>Indemnités</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody class='internal'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='6'>Total</td>\n                <td id='km_internal_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </tr>\n        </tfoot>\n    </table>\n    <br/>\n    <table class=\"opa table table-striped table-bordered table-condensed\">\n        <caption>\n            Frais kilométriques concernant directement votre activité auprès de vos clients\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </caption>\n        <thead>\n            <th>Date</th>\n            <th>Type</th>\n            <th>Prestation</th>\n            <th>Point de départ</th>\n            <th>Point d'arrivée</th>\n            <th>Kms</th>\n            <th>Indemnités</th>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody class='activity'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='6'>Total</td>\n                <td id='km_activity_total'></td>\n";
  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            </tr>\n        </tfoot>\n    </table>\n</div>\n";
},"useData":true});
})();