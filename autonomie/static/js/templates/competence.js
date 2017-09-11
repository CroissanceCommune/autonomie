(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['item_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=helpers.blockHelperMissing, alias5=container.escapeExpression, buffer = 
  "            <th ";
  stack1 = ((helper = (helper = helpers.is_reference || (depth0 != null ? depth0.is_reference : depth0)) != null ? helper : alias2),(options={"name":"is_reference","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.is_reference) { stack1 = alias4.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += ">\n                "
    + alias5(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + " ("
    + alias5(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + ") ";
  stack1 = ((helper = (helper = helpers.is_reference || (depth0 != null ? depth0.is_reference : depth0)) != null ? helper : alias2),(options={"name":"is_reference","hash":{},"fn":container.program(4, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.is_reference) { stack1 = alias4.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n            </th>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "style=\"background-color: #baff87\"";
},"4":function(container,depth0,helpers,partials,data) {
    return "<span class='help-block'>Niveau de référence</span>";
},"6":function(container,depth0,helpers,partials,data) {
    return "#baff87";
},"8":function(container,depth0,helpers,partials,data) {
    return "#c43c35;color:#fff;";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<h3>Évaluation de la compétence : "
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</h3>\n<h4>Pour l'échéance : "
    + alias4(((helper = (helper = helpers.deadline_label || (depth0 != null ? depth0.deadline_label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"deadline_label","hash":{},"data":data}) : helper)))
    + "</h4>\n<form id=\"item_form\">\n<div class=\"panel panel-default\">\n    <table class=\"table table-bordered table-striped table-rounded\">\n        <thead>\n            <th>Sous-Compétence</th>\n";
  stack1 = ((helper = (helper = helpers.scales || (depth0 != null ? depth0.scales : depth0)) != null ? helper : alias2),(options={"name":"scales","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.scales) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            <th>Argumentation/preuves</th>\n        </thead>\n        <tbody>\n        </tbody>\n    </table>\n    <div class='panel-footer text-center' style='background-color: "
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.is_ok_average : depth0),{"name":"if","hash":{},"fn":container.program(6, data, 0),"inverse":container.program(8, data, 0),"data":data})) != null ? stack1 : "")
    + "'>\n        <b>Évaluation : "
    + alias4(((helper = (helper = helpers.average_level || (depth0 != null ? depth0.average_level : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"average_level","hash":{},"data":data}) : helper)))
    + "</b>\n    </div>\n</div>\n<div class='form-group'>\n    <label for=\"comments\">Axes de progrès pour cette échéance</label>\n    <textarea name='progress' class='form-control'>"
    + alias4(((helper = (helper = helpers.progress || (depth0 != null ? depth0.progress : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"progress","hash":{},"data":data}) : helper)))
    + "</textarea>\n</div>\n<button type='button' class='btn btn-primary'>OK</button>\n</form>\n";
},"useData":true});
templates['item_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Compétences à évaluer</h4>\n<ul class=\"nav nav-pills nav-stacked\">\n</ul>\n";
},"useData":true});
templates['item.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<a href=\"#/items/"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "/edit\" ><i class='fa fa-caret-square-o-right'></i>&nbsp;"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</a>\n";
},"useData":true});
templates['subitem.mustache'] = template({"1":function(container,depth0,helpers,partials,data,blockParams,depths) {
    var stack1, helper, options, alias1=container.escapeExpression, alias2=depth0 != null ? depth0 : (container.nullContext || {}), alias3=helpers.helperMissing, alias4="function", buffer = 
  "<td>\n    <input\n        type=\"radio\"\n        name=\"subitem_"
    + alias1(container.lambda((depths[1] != null ? depths[1].id : depths[1]), depth0))
    + "\"\n        ";
  stack1 = ((helper = (helper = helpers.is_selected || (depth0 != null ? depth0.is_selected : depth0)) != null ? helper : alias3),(options={"name":"is_selected","hash":{},"fn":container.program(2, data, 0, blockParams, depths),"inverse":container.noop,"data":data}),(typeof helper === alias4 ? helper.call(alias2,options) : helper));
  if (!helpers.is_selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n        value=\""
    + alias1(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias3),(typeof helper === alias4 ? helper.call(alias2,{"name":"value","hash":{},"data":data}) : helper)))
    + "\">\n    </input>\n</td>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "checked";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data,blockParams,depths) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<td>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</td>\n";
  stack1 = ((helper = (helper = helpers.scales || (depth0 != null ? depth0.scales : depth0)) != null ? helper : alias2),(options={"name":"scales","hash":{},"fn":container.program(1, data, 0, blockParams, depths),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.scales) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "<td>\n<div class='form-group'>\n    <textarea name='comments' class='form-control'>"
    + alias4(((helper = (helper = helpers.comments || (depth0 != null ? depth0.comments : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"comments","hash":{},"data":data}) : helper)))
    + "</textarea>\n</div>\n</td>\n";
},"useData":true,"useDepths":true});
})();