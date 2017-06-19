(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['csv_import.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "<div class=\"text-center btn btn-warning\">\n<i class=\"fa fa-cog fa-spin fa-4x\"></i>\n<br />\n<b>L'import est en cours</b>\n</div>\n";
  },"3":function(depth0,helpers,partials,data) {
  var stack1, buffer = "\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.failed : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"4":function(depth0,helpers,partials,data) {
  return "<div class=\"text-center btn btn-danger\">\n<i class=\"fa fa-warning fa-4x\"></i>\n<br />\n<b>L'import a échoué</b>\n</div>\n";
  },"6":function(depth0,helpers,partials,data) {
  return "\n<div class=\"text-center btn btn-success\">\n<i class=\"fa fa-check fa-4x\"></i>\n<br />\n<b>L'import s'est déroulé avec succès</b>\n</div>\n\n";
  },"8":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n<div class='col-md-6'>\n<h4>Messages</h4>\n"
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
  buffer += "</div>\n<div class='col-md-6'>\n<h4>Télécharger des données</h4>\n";
  stack1 = ((helper = (helper = helpers.has_unhandled_datas || (depth0 != null ? depth0.has_unhandled_datas : depth0)) != null ? helper : helperMissing),(options={"name":"has_unhandled_datas","hash":{},"fn":this.program(13, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_unhandled_datas) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "<hr>\n";
  stack1 = ((helper = (helper = helpers.has_errors || (depth0 != null ? depth0.has_errors : depth0)) != null ? helper : helperMissing),(options={"name":"has_errors","hash":{},"fn":this.program(15, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_errors) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n</div>\n";
},"9":function(depth0,helpers,partials,data) {
  return "Aucun message n'a été retourné\n";
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
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n<div class='col-md-6'>\n<h2>Import de données</h2>\n<ul>\n<li>Identifiant de la tâche : "
    + escapeExpression(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Initialisée le : "
    + escapeExpression(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Mise à jour le : "
    + escapeExpression(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n</ul>\n</div>\n<div class=\"col-md-3 col-md-offset-3\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.running : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n</div>\n<hr />\n";
  stack1 = ((helper = (helper = helpers.running || (depth0 != null ? depth0.running : depth0)) != null ? helper : helperMissing),(options={"name":"running","hash":{},"fn":this.noop,"inverse":this.program(8, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.running) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
templates['file_generation.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "<div class=\"text-center btn btn-warning\">\n<i class=\"fa fa-cog fa-spin fa-4x\"></i>\n<br />\n<b>La génération de fichier est en cours</b>\n</div>\n";
  },"3":function(depth0,helpers,partials,data) {
  var stack1, buffer = "\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.failed : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"4":function(depth0,helpers,partials,data) {
  return "    <div class=\"text-center btn btn-danger\">\n        <i class=\"fa fa-warning fa-4x\"></i>\n        <br />\n        <b>La génération de fichier a échoué</b>\n    </div>\n";
  },"6":function(depth0,helpers,partials,data) {
  return "    <div class=\"text-center btn btn-success\">\n        <i class=\"fa fa-check fa-4x\"></i>\n        <br />\n        <b>L'import s'est déroulé avec succès</b>\n    </div>\n";
  },"8":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n    <div class='col-md-6'>\n        <h4>Télécharger votre fichier</h4>\n        <a href=\"/cooked/"
    + escapeExpression(((helper = (helper = helpers.filename || (depth0 != null ? depth0.filename : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"filename","hash":{},"data":data}) : helper)))
    + "\" target=\"_blank\" class=\"btn btn-success btn-large\">\n        <i class='glyphicon glyphicon-download'></i> Télécharger\n        </a>\n    </div>\n    <div class='col-md-6'>\n    <h4>Messages</h4>\n    "
    + escapeExpression(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_message || (depth0 != null ? depth0.has_message : depth0)) != null ? helper : helperMissing),(options={"name":"has_message","hash":{},"fn":this.noop,"inverse":this.program(9, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_message) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  buffer += "    <h4>Erreurs</h4>\n    "
    + escapeExpression(((helper = (helper = helpers.err_message || (depth0 != null ? depth0.err_message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"err_message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_err_message || (depth0 != null ? depth0.has_err_message : depth0)) != null ? helper : helperMissing),(options={"name":"has_err_message","hash":{},"fn":this.noop,"inverse":this.program(11, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.has_err_message) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n</div>\n";
},"9":function(depth0,helpers,partials,data) {
  return "    Aucun message n'a été retourné\n";
  },"11":function(depth0,helpers,partials,data) {
  return "    Aucune erreur n'a été retournée\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n<div class='col-md-6'>\n<h2>Génération de fichier</h2>\n<ul>\n<li>Identifiant de la tâche : "
    + escapeExpression(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Initialisée le : "
    + escapeExpression(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Mise à jour le : "
    + escapeExpression(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n</ul>\n</div>\n<div class=\"col-md-3 col-md-offset-3\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.running : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </div>\n</div>\n<hr />\n";
  stack1 = ((helper = (helper = helpers.running || (depth0 != null ? depth0.running : depth0)) != null ? helper : helperMissing),(options={"name":"running","hash":{},"fn":this.noop,"inverse":this.program(8, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.running) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer + "\n";
},"useData":true});
templates['mailing.mustache'] = template({"1":function(depth0,helpers,partials,data) {
  return "<div class=\"btn text-center btn-warning\">\n<i class=\"fa fa-cog fa-spin fa-4x\"></i>\n<br />\n<b>L'envoi est en cours</b>\n</div>\n";
  },"3":function(depth0,helpers,partials,data) {
  var stack1, buffer = "\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.failed : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"4":function(depth0,helpers,partials,data) {
  return "<div class=\"btn text-center btn-danger\">\n<i class=\"fa fa-warning fa-4x\"></i>\n<br />\n<b>L'envoi a échoué</b>\n</div>\n";
  },"6":function(depth0,helpers,partials,data) {
  return "\n<div class=\"btn text-center btn-success\">\n<i class=\"fa fa-check fa-4x\"></i>\n<br />\n<b>L'envoi s'est déroulé avec succès</b>\n</div>\n\n";
  },"8":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n<div class='col-md-12'>\n<h4>Messages</h4>\n"
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
  return buffer + "</div>\n</div>\n";
},"9":function(depth0,helpers,partials,data) {
  return "Aucun message n'a été retourné\n";
  },"11":function(depth0,helpers,partials,data) {
  return "Aucune erreur n'a été retournée\n";
  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n<div class='col-md-6'>\n<h2>Envoi de document par mail</h2>\n<ul>\n<li>Identifiant de la tâche : "
    + escapeExpression(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Initialisée le : "
    + escapeExpression(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Mise à jour le : "
    + escapeExpression(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n</ul>\n</div>\n<div class=\"col-md-3 col-md-offset-3\">\n";
  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.running : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
  if (stack1 != null) { buffer += stack1; }
  buffer += "</div>\n</div>\n<hr />\n";
  stack1 = ((helper = (helper = helpers.running || (depth0 != null ? depth0.running : depth0)) != null ? helper : helperMissing),(options={"name":"running","hash":{},"fn":this.noop,"inverse":this.program(8, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
  if (!helpers.running) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
  if (stack1 != null) { buffer += stack1; }
  return buffer;
},"useData":true});
})();