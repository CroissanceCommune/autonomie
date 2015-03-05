(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
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
})();