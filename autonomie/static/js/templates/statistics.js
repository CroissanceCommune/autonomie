(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['entry_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Entrées statistiques</h4>\n<table class=\"table table-bordered table-condensed\">\n    <thead>\n        <th>Intitulé</th>\n        <th>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n";
  },"useData":true});
templates['entry.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td>\n"
    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
    + "\n</td>\n<td>\n# TODO url vers csv, edit\n</td>\n";
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