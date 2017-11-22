(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['csv_import.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center\">\n            <i class=\"fa fa-clock-o fa-4x\"></i>\n            <br />\n            <b>L'import est en attente de traitement</b>\n            </div>\n";
},"3":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.running : depth0),{"name":"if","hash":{},"fn":container.program(4, data, 0),"inverse":container.program(6, data, 0),"data":data})) != null ? stack1 : "");
},"4":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-warning\">\n            <i class=\"fa fa-cog fa-spin fa-4x\"></i>\n            <br />\n            <b>L'import est en cours</b>\n            </div>\n";
},"6":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.failed : depth0),{"name":"if","hash":{},"fn":container.program(7, data, 0),"inverse":container.program(9, data, 0),"data":data})) != null ? stack1 : "");
},"7":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-danger\">\n            <i class=\"fa fa-warning fa-4x\"></i>\n            <br />\n            <b>L'import a échoué</b>\n            </div>\n";
},"9":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-success\">\n            <i class=\"fa fa-check fa-4x\"></i>\n            <br />\n            <b>L'import s'est déroulé avec succès</b>\n            </div>\n";
},"11":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, alias5=helpers.blockHelperMissing, buffer = 
  "    <div class='row'>\n    <div class='col-md-6'>\n    <h4>Messages</h4>\n    "
    + alias4(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_message || (depth0 != null ? depth0.has_message : depth0)) != null ? helper : alias2),(options={"name":"has_message","hash":{},"fn":container.noop,"inverse":container.program(12, data, 0),"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.has_message) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "    <h4>Erreurs</h4>\n    "
    + alias4(((helper = (helper = helpers.err_message || (depth0 != null ? depth0.err_message : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"err_message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_err_message || (depth0 != null ? depth0.has_err_message : depth0)) != null ? helper : alias2),(options={"name":"has_err_message","hash":{},"fn":container.noop,"inverse":container.program(14, data, 0),"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.has_err_message) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "    </div>\n    <div class='col-md-6'>\n    <h4>Télécharger des données</h4>\n";
  stack1 = ((helper = (helper = helpers.has_unhandled_datas || (depth0 != null ? depth0.has_unhandled_datas : depth0)) != null ? helper : alias2),(options={"name":"has_unhandled_datas","hash":{},"fn":container.program(16, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.has_unhandled_datas) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "    <hr>\n";
  stack1 = ((helper = (helper = helpers.has_errors || (depth0 != null ? depth0.has_errors : depth0)) != null ? helper : alias2),(options={"name":"has_errors","hash":{},"fn":container.program(18, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.has_errors) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </div>\n    </div>\n";
},"12":function(container,depth0,helpers,partials,data) {
    return "    Aucun message n'a été retourné\n";
},"14":function(container,depth0,helpers,partials,data) {
    return "    Aucune erreur n'a été retournée\n";
},"16":function(container,depth0,helpers,partials,data) {
    var helper;

  return "    Télécharger les données du fichier qui n'ont pas été importées :\n    <a class='btn btn-warning' href=\""
    + container.escapeExpression(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"url","hash":{},"data":data}) : helper)))
    + "?action=unhandled.csv\">Télécharger</a>\n";
},"18":function(container,depth0,helpers,partials,data) {
    var helper;

  return "    Télécharger les lignes du fichier contenant des erreurs :\n    <a class='btn btn-danger' href=\""
    + container.escapeExpression(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"url","hash":{},"data":data}) : helper)))
    + "?action=errors.csv\">Télécharger</a>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<h1>Import de données</h1>\n<div class='row'>\n<div class='col-md-6'>\n<ul>\n<li>Identifiant de la tâche : "
    + alias4(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Initialisée le : "
    + alias4(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n<li>Mise à jour le : "
    + alias4(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n</ul>\n</div>\n<div class=\"col-md-3 col-md-offset-3\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.waiting : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.program(3, data, 0),"data":data})) != null ? stack1 : "")
    + "</div>\n</div>\n<hr />\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.finished : depth0),{"name":"if","hash":{},"fn":container.program(11, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['file_generation.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center\">\n            <i class=\"fa fa-clock-o fa-4x\"></i>\n            <br />\n            <b>La génération est en attente de traitement</b>\n            </div>\n";
},"3":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.running : depth0),{"name":"if","hash":{},"fn":container.program(4, data, 0),"inverse":container.program(6, data, 0),"data":data})) != null ? stack1 : "");
},"4":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-warning\">\n            <i class=\"fa fa-cog fa-spin fa-4x\"></i>\n            <br />\n            <b>La génération est en cours</b>\n            </div>\n";
},"6":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.failed : depth0),{"name":"if","hash":{},"fn":container.program(7, data, 0),"inverse":container.program(9, data, 0),"data":data})) != null ? stack1 : "");
},"7":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-danger\">\n            <i class=\"fa fa-warning fa-4x\"></i>\n            <br />\n            <b>La génération de fichier a échoué</b>\n            </div>\n";
},"9":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-success\">\n            <i class=\"fa fa-check fa-4x\"></i>\n            <br />\n            <b>La génération de fichier s'est déroulée avec succès</b>\n            </div>\n";
},"11":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=depth0 != null ? depth0 : (container.nullContext || {});

  return "<div class='row'>\n    <div class='col-md-6'>\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.filename : depth0),{"name":"if","hash":{},"fn":container.program(12, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "    </div>\n    <div class='col-md-6'>\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.has_message : depth0),{"name":"if","hash":{},"fn":container.program(14, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.has_err_message : depth0),{"name":"if","hash":{},"fn":container.program(16, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "    </div>\n</div>\n";
},"12":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "        <script type='text/javascript'>\n            var win = window.open(\"/cooked/"
    + alias4(((helper = (helper = helpers.filename || (depth0 != null ? depth0.filename : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"filename","hash":{},"data":data}) : helper)))
    + "\", \"_self\");\n            setTimeout(function(){win.close(); window.close()}, 1000);\n        </script>\n        <h4>Télécharger votre fichier</h4>\n        <a href=\"/cooked/"
    + alias4(((helper = (helper = helpers.filename || (depth0 != null ? depth0.filename : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"filename","hash":{},"data":data}) : helper)))
    + "\" target=\"_blank\" class=\"btn btn-success btn-large\">\n        <i class='glyphicon glyphicon-download'></i> Télécharger\n        </a>\n";
},"14":function(container,depth0,helpers,partials,data) {
    var helper;

  return "        <h4>Messages</h4>\n        "
    + container.escapeExpression(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"message","hash":{},"data":data}) : helper)))
    + "\n";
},"16":function(container,depth0,helpers,partials,data) {
    var helper;

  return "        <h4>Erreurs</h4>\n        "
    + container.escapeExpression(((helper = (helper = helpers.err_message || (depth0 != null ? depth0.err_message : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"err_message","hash":{},"data":data}) : helper)))
    + "\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<h1>Génération de fichier</h1>\n<div class='row'>\n    <div class='col-md-6'>\n        <ul>\n        <li>Identifiant de la tâche : "
    + alias4(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n        <li>Initialisée le : "
    + alias4(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n        <li>Mise à jour le : "
    + alias4(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n        </ul>\n    </div>\n    <div class=\"col-md-3 col-md-offset-3\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.waiting : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.program(3, data, 0),"data":data})) != null ? stack1 : "")
    + "    </div>\n</div>\n<hr />\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.finished : depth0),{"name":"if","hash":{},"fn":container.program(11, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['mailing.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center\">\n            <i class=\"fa fa-clock-o fa-4x\"></i>\n            <br />\n            <b>L'envoi est en attente de traitement</b>\n            </div>\n";
},"3":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.running : depth0),{"name":"if","hash":{},"fn":container.program(4, data, 0),"inverse":container.program(6, data, 0),"data":data})) != null ? stack1 : "");
},"4":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-warning\">\n            <i class=\"fa fa-cog fa-spin fa-4x\"></i>\n            <br />\n            <b>Envoi est en cours</b>\n            </div>\n";
},"6":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers["if"].call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.failed : depth0),{"name":"if","hash":{},"fn":container.program(7, data, 0),"inverse":container.program(9, data, 0),"data":data})) != null ? stack1 : "");
},"7":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-danger\">\n            <i class=\"fa fa-warning fa-4x\"></i>\n            <br />\n            <b>L'envoi a échoué</b>\n            </div>\n";
},"9":function(container,depth0,helpers,partials,data) {
    return "            <div class=\"text-center text-success\">\n            <i class=\"fa fa-check fa-4x\"></i>\n            <br />\n            <b>L'envoi s'est déroulé avec succès</b>\n            </div>\n";
},"11":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, alias5=helpers.blockHelperMissing, buffer = 
  "<div class='row'>\n<div class='col-md-12'>\n<h4>Messages</h4>\n"
    + alias4(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_message || (depth0 != null ? depth0.has_message : depth0)) != null ? helper : alias2),(options={"name":"has_message","hash":{},"fn":container.noop,"inverse":container.program(12, data, 0),"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.has_message) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "<h4>Erreurs</h4>\n"
    + alias4(((helper = (helper = helpers.err_message || (depth0 != null ? depth0.err_message : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"err_message","hash":{},"data":data}) : helper)))
    + "\n";
  stack1 = ((helper = (helper = helpers.has_err_message || (depth0 != null ? depth0.has_err_message : depth0)) != null ? helper : alias2),(options={"name":"has_err_message","hash":{},"fn":container.noop,"inverse":container.program(14, data, 0),"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.has_err_message) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "</div>\n</div>\n";
},"12":function(container,depth0,helpers,partials,data) {
    return "Aucun message n'a été retourné\n";
},"14":function(container,depth0,helpers,partials,data) {
    return "Aucune erreur n'a été retournée\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<div class='row'>\n    <div class='col-md-6'>\n        <h2>Envoi de document par mail</h2>\n        <ul>\n        <li>Identifiant de la tâche : "
    + alias4(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"jobid","hash":{},"data":data}) : helper)))
    + " </li>\n        <li>Initialisée le : "
    + alias4(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"created_at","hash":{},"data":data}) : helper)))
    + " </li>\n        <li>Mise à jour le : "
    + alias4(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"updated_at","hash":{},"data":data}) : helper)))
    + " </li>\n        </ul>\n    </div>\n    <div class=\"col-md-3 col-md-offset-3\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.waiting : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.program(3, data, 0),"data":data})) != null ? stack1 : "")
    + "    </div>\n</div>\n<hr />\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.finished : depth0),{"name":"if","hash":{},"fn":container.program(11, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
})();