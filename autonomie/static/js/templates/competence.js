(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['item_form.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, escapeExpression=this.escapeExpression, buffer = "            <th ";
  stack1 = ((helper = (helper = helpers.is_reference || (depth0 != null ? depth0.is_reference : depth0)) != null ? helper : helperMissing),(options={"name":"is_reference","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.is_reference) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += ">\n                "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + " ("
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + ") ";
  stack1 = ((helper = (helper = helpers.is_reference || (depth0 != null ? depth0.is_reference : depth0)) != null ? helper : helperMissing),(options={"name":"is_reference","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.is_reference) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n            </th>\n";
},"2":function(depth0,helpers,partials,data) {
  return "style=\"background-color: #baff87\"";
  },"4":function(depth0,helpers,partials,data) {
  return "<span class='help-block'>Niveau de référence</span>";
  },"6":function(depth0,helpers,partials,data) {
  return "#baff87";
  },"8":function(depth0,helpers,partials,data) {
  return "#c43c35;color:#fff;";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<h3>Évaluation de la compétence : "
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "</h3>\n<h4>Pour l'échéance : "
    + escapeExpression(((helper = (helper = helpers.deadline_label || (depth0 != null ? depth0.deadline_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"deadline_label","hash":{},"data":data}) : helper)))
    + "</h4>\n<form id=\"item_form\">\n<div class=\"panel panel-default\">\n    <table class=\"table table-bordered table-striped table-rounded\">\n        <thead>\n            <th>Sous-Compétence</th>\n";
  stack1 = ((helper = (helper = helpers.scales || (depth0 != null ? depth0.scales : depth0)) != null ? helper : helperMissing),(options={"name":"scales","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.scales) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "        </thead>\n        <tbody>\n        </tbody>\n    </table>\n    <div class='panel-footer text-center' style='background-color: ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_ok_average : depth0), {"name":"if","hash":{},"fn":this.program(6, data),"inverse":this.program(8, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "'>\n        <b>Évaluation : "
    + escapeExpression(((helper = (helper = helpers.average_level || (depth0 != null ? depth0.average_level : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"average_level","hash":{},"data":data}) : helper)))
    + "</b>\n    </div>\n</div>\n<div class='form-group'>\n    <label for=\"comments\">Argumentaires pour cette échéance</label>\n    <textarea name='comments' class='form-control'>"
    + escapeExpression(((helper = (helper = helpers.comments || (depth0 != null ? depth0.comments : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"comments","hash":{},"data":data}) : helper)))
    + "</textarea>\n</div>\n<div class='form-group'>\n    <label for=\"comments\">Axes de progrès pour cette échéance</label>\n    <textarea name='progress' class='form-control'>"
    + escapeExpression(((helper = (helper = helpers.progress || (depth0 != null ? depth0.progress : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"progress","hash":{},"data":data}) : helper)))
    + "</textarea>\n</div>\n<button type='button' class='btn btn-primary'>OK</button>\n</form>\n";
},"useData":true});
templates['item_list.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<h4>Compétences à évaluer</h4>\n<ul class=\"nav nav-pills nav-stacked\">\n</ul>\n";
  },"useData":true});
templates['item.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<a href=\"#/items/"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "/edit\" ><i class='fa fa-caret-square-o-right'></i>&nbsp;"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "</a>\n";
},"useData":true});
templates['subitem.mustache'] = template({"1":function(depth0,helpers,partials,data,depths) {
  var stack1, helper, options, lambda=this.lambda, escapeExpression=this.escapeExpression, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>\n    <input\n        type=\"radio\"\n        name=\"subitem_"
    + escapeExpression(lambda((depths[1] != null ? depths[1].id : depths[1]), depth0))
    + "\"\n        ";
  stack1 = ((helper = (helper = helpers.is_selected || (depth0 != null ? depth0.is_selected : depth0)) != null ? helper : helperMissing),(options={"name":"is_selected","hash":{},"fn":this.program(2, data, depths),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.is_selected) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n        value=\""
    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
    + "\">\n    </input>\n</td>\n";
},"2":function(depth0,helpers,partials,data) {
  return "checked";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>"
    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
    + "</td>\n";
  stack1 = ((helper = (helper = helpers.scales || (depth0 != null ? depth0.scales : depth0)) != null ? helper : helperMissing),(options={"name":"scales","hash":{},"fn":this.program(1, data, depths),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.scales) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true,"useDepths":true});
})();