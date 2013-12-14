(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['expenseForm.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, self=this, blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<button class='btn btn-block btn-primary' onclick=\"$('#bookmarks').toggle();\" type='button'>Mes Favoris     >>></button>\n<div id='bookmarks' class='well' style='display:none'>\n<table class=\"table table-condensed table-stripped table-bordered\">\n";
  options = {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data};
  if (stack1 = helpers.bookmark_options) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.bookmark_options); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.bookmark_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</table>\n</div>\n<hr />\n<br />\n";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<tr>\n<td>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  if (stack1 = helpers.attributes) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.attributes); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.attributes) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</td>\n<td>\n<a class=\"btn btn-mini edit\" data-cid='";
  if (stack1 = helpers.cid) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.cid); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'>\n    <i class=\"icon-ok\"></i>\n</a>\n<a class=\"btn btn-mini delete\"  data-cid='";
  if (stack1 = helpers.cid) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.cid); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'>\n    <i class=\"icon-remove-sign\"></i>\n</a>\n</td>\n</tr>\n";
  return buffer;
  }
function program3(depth0,data) {
  
  var buffer = "", stack1;
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + " - HT:";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + " € - TVA:";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + " € ("
    + escapeExpression(((stack1 = ((stack1 = (depth0 && depth0.type)),stack1 == null || stack1 === false ? stack1 : stack1.label)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + ") ";
  return buffer;
  }

function program5(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<label class=\"radio\">\n<input type='radio' name='category' value='";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ";
  options = {hash:{},inverse:self.noop,fn:self.program(6, program6, data),data:data};
  if (stack1 = helpers.selected) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.selected); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "> ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.label); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\n</label>\n";
  return buffer;
  }
function program6(depth0,data) {
  
  
  return "checked";
  }

function program8(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<option value='";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ";
  options = {hash:{},inverse:self.noop,fn:self.program(9, program9, data),data:data};
  if (stack1 = helpers.selected) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.selected); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += ">";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.label); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</option>\n";
  return buffer;
  }
function program9(depth0,data) {
  
  
  return "selected='true'";
  }

  buffer += "<form id='expenseForm' class='form form-horizontal' action='#' onsubmit='return false;'>\n\n";
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='category'>Catégorie de frais</label>\n<div class='controls'>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data};
  if (stack1 = helpers.category_options) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.category_options); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.category_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n</div>\n\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='type_id'>Type de frais</label>\n<div class='controls'>\n<select class='input-xxlarge' name='type_id'>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(8, program8, data),data:data};
  if (stack1 = helpers.type_options) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.type_options); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</select>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='altdate'>Date</label>\n<div class='controls'>\n<input name=\"altdate\" class=\"input-small\" type=\"text\">\n<input name=\"date\" class=\"input-small\" type=\"hidden\">\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='description'>Description</label>\n<div class='controls'>\n<input type='text' class='input-xxlarge' name='description' value='";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='ht'>Montant HT</label>\n<div class='controls'>\n<div class=\"input-append\">\n    <input type='text' class='input-small' name='ht' value='";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='tva'>Montant de la Tva</label>\n<div class='controls'>\n<div class=\"input-append\">\n<input type='text' class='input-small' name='tva' value='";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
  return buffer;
  });
templates['expensetel.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, self=this, blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<td><div class='control-group'><div class='controls'><input type='text' class='input-small' value='";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' name='ht'/></div></div></td>\n<td><div class='control-group'><div class='controls'><input type='text' class='input-small' value='";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' name='tva'/></div></div></td>\n<td><span class='total'>";
  if (stack1 = helpers.total) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.total); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</span></td>\n<td class=\"hidden-print\">\n<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a>\n</td>\n";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<td>";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.total) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.total); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n";
  return buffer;
  }

  buffer += "<td colspan='3'>";
  if (stack1 = helpers.typelabel) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.typelabel); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  options = {hash:{},inverse:self.program(3, program3, data),fn:self.noop,data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });
templates['expenseTelForm.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, self=this, blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<option value='";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ";
  options = {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data};
  if (stack1 = helpers.selected) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.selected); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += ">";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.label); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</option>\n";
  return buffer;
  }
function program2(depth0,data) {
  
  
  return "selected='true'";
  }

  buffer += "<form id='expenseTelForm' class='form form-horizontal' action='#' onsubmit='return false;'>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='type_id'>Type de frais</label>\n<div class='controls'>\n<select class='input-xlarge' name='type_id'>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.type_options) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.type_options); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</select>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='description'>Description</label>\n<div class='controls'>\n<input type='text' class='input-xlarge' name='description' value='";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='ht'>Montant HT</label>\n<div class='controls'>\n<div class=\"input-append\">\n    <input type='text' class='input-small' name='ht' value='";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='tva'>Montant de la Tva</label>\n<div class='controls'>\n<div class=\"input-append\">\n<input type='text' class='input-small' name='tva' value='";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' /><span class=\"add-on\">&euro;</span>\n</div>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
  return buffer;
  });
templates['expenseKmList.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, self=this, functionType="function", blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  
  return "\n            <div class=\"inline-element\">\n<a href=\"#kmlines/add/1\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n            ";
  }

function program3(depth0,data) {
  
  
  return "\n            <th class=\"hidden-print\">Actions</th>\n            ";
  }

function program5(depth0,data) {
  
  
  return "\n                <td class=\"hidden-print\"></td>\n                ";
  }

function program7(depth0,data) {
  
  
  return "\n            <div class=\"inline-element\">\n<a href=\"#kmlines/add/2\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n            ";
  }

  buffer += "<div>\n\n    <table class=\"opa table table-striped table-bordered table-condensed\">\n        <caption>\n        Frais kilométriques liés au fonctionnement de l'entreprise\n            ";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </caption>\n        <thead>\n            <th>Date</th>\n            <th>Type</th>\n            <th>Prestation</th>\n            <th>Point de départ</th>\n            <th>Point d'arrivée</th>\n            <th>Kms</th>\n            <th>Indemnités</th>\n            ";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </thead>\n        <tbody class='internal'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='6'>Total</td>\n                <td id='km_internal_total'></td>\n                ";
  options = {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            </tr>\n        </tfoot>\n    </table>\n    <br/>\n    <table class=\"opa table table-striped table-bordered table-condensed\">\n        <caption>\n            Frais concernant directement votre activité auprès de vos clients\n            ";
  options = {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </caption>\n        <thead>\n            <th>Date</th>\n            <th>Type</th>\n            <th>Prestation</th>\n            <th>Point de départ</th>\n            <th>Point d'arrivée</th>\n            <th>Kms</th>\n            <th>Indemnités</th>\n            ";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </thead>\n        <tbody class='activity'>\n        </tbody>\n        <tfoot>\n            <tr>\n                <td colspan='6'>Total</td>\n                <td id='km_activity_total'></td>\n                ";
  options = {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            </tr>\n        </tfoot>\n    </table>\n</div>\n";
  return buffer;
  });
templates['serverMessage.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, self=this, functionType="function", blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression;

function program1(depth0,data) {
  
  
  return "\nclass=\"alert alert-error\">\n<i class=\"icon-warning-sign\"></i>\n";
  }

function program3(depth0,data) {
  
  
  return "\nclass=\"alert alert-success\">\n<i class=\"icon-ok\"></i>\n";
  }

  buffer += "<div\n";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.error) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.error); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.error) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  options = {hash:{},inverse:self.program(3, program3, data),fn:self.noop,data:data};
  if (stack1 = helpers.error) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.error); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.error) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n<button class=\"close\" data-dismiss=\"alert\" type=\"button\">×</button>\n";
  if (stack1 = helpers.msg) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.msg); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\n</div>\n";
  return buffer;
  });
templates['expenseKm.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, self=this, blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<td class=\"hidden-print\"><a class='btn' href='";
  if (stack1 = helpers.edit_url) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.edit_url); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>\n<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</td>\n";
  return buffer;
  }

  buffer += "<td>";
  if (stack1 = helpers.altdate) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.altdate); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.typelabel) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.typelabel); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.start) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.start); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.end) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.end); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.km) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.km); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.total) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.total); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });
templates['holiday.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<td>";
  if (stack1 = helpers.alt_start_date) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.alt_start_date); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.alt_end_date) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.alt_end_date); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td><a class='btn edit'><i class='icon icon-pencil'></i>&nbsp;Éditer</a><a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a></td>\n";
  return buffer;
  });
templates['holidayForm.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<form id='holidayForm' class='form' action='#' onsubmit='return false;'>\n<div class=\"control-group\">\n<label class=\"control-label\" for='alt_start_date'>Début</label>\n<div class='controls'>\n    <input name=\"alt_start_date\" class=\"input-small\" type=\"text\">\n    <input name=\"start_date\" type=\"hidden\">\n</div>\n</div>\n<div class=\"control-group\">\n<label class=\"control-label\" for='alt_end_date'>Fin</label>\n<div class='controls'>\n    <input name=\"alt_end_date\" class=\"input-small\" type=\"text\">\n    <input name=\"end_date\" type=\"hidden\">\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
  });
templates['holidayList.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div>\n    <table class=\"opa table table-bordered table-condensed\">\n        <caption>\n        Vos congés\n            <div class=\"inline-element\">\n                <a class='btn add' title=\"Déclarer un congés\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n        </caption>\n        <thead>\n            <th>Date de début</th>\n            <th>Date de fin</th>\n            <th>Actions</th>\n        </thead>\n        <tbody>\n        </tbody>\n    </table>\n</div>\n";
  });
templates['expense.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, self=this, blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<td class='hidden-print'><a class='btn' href='";
  if (stack1 = helpers.edit_url) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.edit_url); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>\n<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a>\n<a class='btn' href='";
  if (stack1 = helpers.bookmark_url) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.bookmark_url); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'><i class='icon-star-empty'></i>&nbsp;Favoris</a>\n</td>\n";
  return buffer;
  }

  buffer += "<td>";
  if (stack1 = helpers.altdate) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.altdate); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.typelabel) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.typelabel); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.total) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.total); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });
templates['expenseorphan.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<td>";
  if (stack1 = helpers.altdate) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.altdate); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.typelabel) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.typelabel); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "(ce type ne semble plus exister)</td>\n<td>";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.ht) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.ht); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.tva) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.tva); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.total) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.total); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n<td class=\"hidden-print\"></td>\n";
  return buffer;
  });
templates['expenseKmForm.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, functionType="function", escapeExpression=this.escapeExpression, self=this, blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<label class=\"radio\">\n<input type='radio' name='category' value='";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ";
  options = {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data};
  if (stack1 = helpers.selected) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.selected); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "> ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.label); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\n</label>\n";
  return buffer;
  }
function program2(depth0,data) {
  
  
  return "checked";
  }

function program4(depth0,data) {
  
  var buffer = "", stack1, options;
  buffer += "\n<label class=\"radio\">\n<input type='radio' name='type_id' value='";
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' ";
  options = {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data};
  if (stack1 = helpers.selected) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.selected); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "> ";
  if (stack1 = helpers.label) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.label); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\n</label>\n";
  return buffer;
  }

  buffer += "<form id='expenseKmForm' class='form' action='#' onsubmit='return false;'>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='category'>Catégorie de frais</label>\n<div class='controls'>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.category_options) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.category_options); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.category_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='type_id'>Véhicule</label>\n<div class='controls'>\n";
  options = {hash:{},inverse:self.noop,fn:self.program(4, program4, data),data:data};
  if (stack1 = helpers.type_options) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.type_options); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.type_options) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='altdate'>Date</label>\n<div class='controls'>\n<input name=\"altdate\" class=\"input-small\" type=\"text\">\n<input name=\"date\" class=\"input-small\" type=\"hidden\">\n</div>\n</div>\n\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='start'>Point de départ</label>\n<div class='controls'>\n<input type='text' class='input-medium' name='start' value='";
  if (stack1 = helpers.start) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.start); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='end'>Point d'arrivée</label>\n<div class='controls'>\n<input type='text' class='input-medium' name='end' value='";
  if (stack1 = helpers.end) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.end); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "'/>\n</div>\n</div>\n\n<div class=\"control-group\">\n<label class=\"control-label\" for='ht'>Nombre de Kilomètres</label>\n<div class='controls'>\n<div class=\"input-append\">\n    <input type='text' class='input-small' name='km' value='";
  if (stack1 = helpers.km) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.km); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' /><span class=\"add-on\">km</span>\n</div>\n</div>\n</div>\n\n<div class='control-group'>\n<label class=\"control-label\" for='description'>Description</label>\n<div class='controls'>\n<input type='text' class='input-xlarge' name='description' value='";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "' />\n<span class=\"help-block\"> Le cas échéant, indiquer la prestation liée à ces frais</span>\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
  return buffer;
  });
templates['expenseList.mustache'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, options, self=this, functionType="function", blockHelperMissing=helpers.blockHelperMissing;

function program1(depth0,data) {
  
  
  return "\n    <div class=\"inline-element\">\n    <a href=\"#lines/add/1\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n    <a href=\"#tel/add\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une lignei de frais téléphonique\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais téléphoniques</a>\n    </div>\n    ";
  }

function program3(depth0,data) {
  
  
  return "\n        <th class=\"hidden-print\">Actions</th>\n            ";
  }

function program5(depth0,data) {
  
  
  return "\n            <td class=\"hidden-print\"></td>\n            ";
  }

function program7(depth0,data) {
  
  
  return "\n    <div class=\"inline-element\">\n    <a href=\"#lines/add/2\" class='btn visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n    </div>\n    ";
  }

function program9(depth0,data) {
  
  
  return "\n        <th class=\"hidden-print\">Actions</th>\n        ";
  }

  buffer += "<div>\n<table class=\"opa table table-bordered table-condensed\">\n    <caption>\n    Frais liés au fonctionnement de l'entreprise\n    ";
  options = {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </caption>\n    <thead>\n        <th>Date</th>\n        <th>Type de frais</th>\n        <th>Description</th>\n        <th>Montant HT</th>\n        <th>Tva</th>\n        <th>Total</th>\n        ";
  options = {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </thead>\n    <tbody class='internal'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='5'>Total</td>\n            <td id='internal_total'></td>\n        ";
  options = {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </tr>\n    </tfoot>\n</table>\n<br />\n<table class=\"opa table table-bordered table-condensed\">\n    <caption>\n    Frais concernant directement votre activité auprès de vos clients\n    ";
  options = {hash:{},inverse:self.noop,fn:self.program(7, program7, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </caption>\n    <thead>\n        <th>Date</th>\n        <th>Type de frais</th>\n        <th>Description</th>\n        <th>Montant HT</th>\n        <th>Tva</th>\n        <th>Total</th>\n        ";
  options = {hash:{},inverse:self.noop,fn:self.program(9, program9, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n    </thead>\n    <tbody class='activity'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='5'>Total</td>\n            <td id='activity_total'></td>\n        ";
  options = {hash:{},inverse:self.noop,fn:self.program(5, program5, data),data:data};
  if (stack1 = helpers.edit) { stack1 = stack1.call(depth0, options); }
  else { stack1 = (depth0 && depth0.edit); stack1 = typeof stack1 === functionType ? stack1.call(depth0, options) : stack1; }
  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </tr>\n    </tfoot>\n</table>\n</div>\n";
  return buffer;
  });
})();