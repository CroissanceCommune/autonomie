(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['criterion_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Critères composant notre entrée statistique\n<a class='btn btn-primary' style='font-size: 10px' href='#entries/add'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-9'>Intitulé</th>\n        <th class='col-xs-3 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n";
  },"useData":true});
templates['criterion.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td>\n"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "\n</td>\n<td class='action'>\n    <a class='btn btn-default btn-sm' href='#entries/"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "/edit' title=\"Modifier cette entrée\">\n        Modifier\n    </a>\n</td>\n";
},"useData":true});
templates['entry_form.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<form >\n    <div class=\"form-group\">\n        <label class='control-label' for=\"title\">Intitulé de l'entrée statistique <b class='required'>*</b></label>\n        <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n        <span class='help-block'>\n            Sera utilisé dans le fichier de sortie\n        </span>\n    </div>\n    <div class=\"form-group\">\n        <label class='control-label' for=\"title\">Description de l'entrée statistique</label>\n        <textarea name='description' class=\"form-control\" id=\"title\" placeholder=\"Description\">"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n    </div>\n    <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n    <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n</form>\n";
},"useData":true});
templates['entry_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Entrées statistiques\n<a class='btn btn-primary' style='font-size: 10px' href='#entries/add'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-9'>Intitulé</th>\n        <th class='col-xs-3 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n";
  },"useData":true});
templates['entry.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td>\n"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "\n</td>\n<td class='action'>\n    <a class='btn btn-default btn-sm' href='#entries/"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "/edit' title=\"Modifier cette entrée\">\n        Modifier\n    </a>\n    <a class='btn btn-default btn-sm' href='"
    + escapeExpression(((helper = (helper = helpers.csv_url || (depth0 != null ? depth0.csv_url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"csv_url","hash":{},"data":data}) : helper)))
    + "' title='Exporter les éléments correspondant à cette entrée statistiques'>\n        Exporter\n    </a>\n    <a class='btn btn-default btn-sm remove' title='Supprimer cette entrée'>\n        Supprimer\n    </a>\n</td>\n";
},"useData":true});
templates['full_entry_form.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<div class='form'>\n    <button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <h4>"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "</h4>\n    <span class='help-block'>"
    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
    + "</span>\n    <div id='criteria'></div>\n    <div id='criterion_form'></div>\n</div>\n";
},"useData":true});
templates['sheet_form.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<h3>\n    "
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "\n    <button class='btn btn-default btn-xs edit' style='font-size:9px' title=\"Éditer le titre de la feuille de statistiques\">\n    <i class=\"glyphicon glyphicon-pencil\" style=\"vertical-align:middle\"> </i>\n    </button>\n</h3>\n";
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
  buffer += "<form class=\"form-inline\"\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += ">\n  <div class=\"form-group\">\n    <label class='control-label' for=\"title\">Intitulé de la feuille de statistique</label>\n    <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n  </div>\n    <button type=\"button\" class=\"btn btn-primary submit\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.program(7, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </button>\n</form>\n";
},"useData":true});
})();