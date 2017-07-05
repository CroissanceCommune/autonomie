(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['paymentAmount.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "has-error";
  },"3":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing;
  stack1 = ((helper = (helper = helpers.amount || (depth0 != null ? depth0.amount : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"amount","hash":{},"data":data}) : helper));
  if (stack1 != null) { return stack1; }
  else { return ''; }
  },"5":function(depth0,helpers,partials,data) {
  return "0,00 €";
  },"7":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "    <span class='help-block'>\n        "
    + escapeExpression(((helper = (helper = helpers.amount_error || (depth0 != null ? depth0.amount_error : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"amount_error","hash":{},"data":data}) : helper)))
    + "\n    </span>\n";
},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class='col-md-2 form-group col-md-offset-2 paymentamount ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount_error : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "'>\n    <input class='input-sm' type='text' name=\"amount\" id=\"amount_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\" value=\"";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.program(5, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></input>\n    <button class='btn btn-info pull-right' type=\"button\" onclick='addPaymentRow({readonly:false, description:\"Paiement\"}, \"#paymentline_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\");'>\n        + Ajouter une échéance\n    </button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount_error : depth0), {"name":"if","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n<div class='col-md-1'>\n    <button type='button' class='close' onclick=\"delRow('paymentline_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "');\">x</button>\n</div>\n";
},"useData":true});
templates['payment.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "has-error";
  },"3":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)));
  },"5":function(depth0,helpers,partials,data) {
  return "Livrable";
  },"7":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "        <span class='help-block'>\n            "
    + escapeExpression(((helper = (helper = helpers.description_error || (depth0 != null ? depth0.description_error : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description_error","hash":{},"data":data}) : helper)))
    + "\n        </span>\n";
},"9":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "value=\""
    + escapeExpression(((helper = (helper = helpers.date || (depth0 != null ? depth0.date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"date","hash":{},"data":data}) : helper)))
    + "\"";
},"11":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "        <span class='help-block'>\n            "
    + escapeExpression(((helper = (helper = helpers.date_error || (depth0 != null ? depth0.date_error : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"date_error","hash":{},"data":data}) : helper)))
    + "\n        </span>\n";
},"13":function(depth0,helpers,partials,data) {
  var stack1, buffer = "    <div class='col-md-2 col-md-offset-2 paymentamount form-group ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount_error : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "'>\n        <div class='input'>";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount : depth0), {"name":"if","hash":{},"fn":this.program(14, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n        <input type='hidden' value=\"";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount : depth0), {"name":"if","hash":{},"fn":this.program(14, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\" name=\"amount\"></input>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount_error : depth0), {"name":"if","hash":{},"fn":this.program(16, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n";
},"14":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing;
  stack1 = ((helper = (helper = helpers.amount || (depth0 != null ? depth0.amount : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"amount","hash":{},"data":data}) : helper));
  if (stack1 != null) { return stack1; }
  else { return ''; }
  },"16":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "        <span class='help-block'>\n            "
    + escapeExpression(((helper = (helper = helpers.amount_error || (depth0 != null ? depth0.amount_error : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"amount_error","hash":{},"data":data}) : helper)))
    + "\n        </span>\n";
},"18":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "    <div class='col-md-2 form-group col-md-offset-2 paymentamount ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount_error : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "'>\n        <input class='input-sm' type='text' name=\"amount\" id=\"amount_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\" value=\"";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount : depth0), {"name":"if","hash":{},"fn":this.program(14, data),"inverse":this.program(19, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\"></input>\n        <button class='btn btn-info pull-right' type=\"button\" onclick='addPaymentRow({readonly:false, description:\"Paiement\"}, \"#paymentline_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\");'>\n            +\n        </button>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount_error : depth0), {"name":"if","hash":{},"fn":this.program(16, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n    <div class='col-md-1'>\n        <button type='button' class='close' onclick=\"delRow('paymentline_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "');\">x</button>\n    </div>\n";
},"19":function(depth0,helpers,partials,data) {
  return "0,00 €";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class='row paymentline' id=\"paymentline_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\">\n    <input type=\"hidden\" name=\"__start__\" value=\"payment_lines:mapping\"/>\n    <div\n    class='col-md-5 form-group ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description_error : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "'>\n        <textarea class=\"form-control\" name=\"description\">";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.program(5, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "\n        </textarea>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description_error : depth0), {"name":"if","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </div>\n    <div class='col-md-2 form-group ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.date_error : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "' id=\"date_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\">\n        <input type=\"hidden\" name=\"__start__\" value=\"date:mapping\"></input>\n        <input class='input-sm' type='text' id=\"date_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "\" name=\"displayDate\" ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.date : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "></input>\n        <input class='form-control' type='hidden' id=\"date_"
    + escapeExpression(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"id","hash":{},"data":data}) : helper)))
    + "_altField\" name=\"date\" ";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.date : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "></input>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.date_error : depth0), {"name":"if","hash":{},"fn":this.program(11, data),"inverse":this.noop,"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "        <input type=\"hidden\" name=\"__end__\" value=\"date:mapping\"></input>\n    </div>\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.readonly : depth0), {"name":"if","hash":{},"fn":this.program(13, data),"inverse":this.program(18, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    <input type=\"hidden\" name=\"__end__\" value=\"payment_lines:mapping\"/>\n</div>\n";
},"useData":true});
templates['tvalist.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class=\"row\">\n<div class=\"col-xs-6\" style=\"text-align:right\">\n    <label>TVA à ";
  stack1 = ((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  buffer += "</label>\n</div>\n<div class='col-xs-6'>\n<div class='input'>";
  stack1 = ((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper));
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n</div>\n</div>\n";
},"useData":true});
})();