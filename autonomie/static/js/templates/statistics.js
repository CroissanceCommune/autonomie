(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['andcriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                    <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<div class='well'>\n<form name='criterion'>\n    <button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset>\n        <legend>\n            "
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "\n        </legend>\n        <div class='alert alert-info'>\n            <ul>\n            <li>1- Configurer vos critères</li>\n            <li>2- Créer une clause 'ET'</li>\n            <li>3- Sélectionner les critères à utiliser dans la clause 'ET'</li>\n            </ul>\n        </div>\n        <div class='row'>\n            <div class=\"form-group col-sm-6\">\n                <label for=\"criteria\">Combiner les critères</label>\n                <select multiple name='criteria' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.criteria_options || (depth0 != null ? depth0.criteria_options : depth0)) != null ? helper : alias2),(options={"name":"criteria_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.criteria_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                </select>\n            </div>\n        </div>\n        <div class=\"form-actions\">\n            <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n            <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n        </div>\n    </fieldset>\n</form>\n</div>\n";
},"useData":true});
templates['boolcriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "            <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<div class='well'>\n<form name='criterion'>\n<button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <input type='hidden' name='key' value='"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset><legend>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</legend>\n    <div class='row'>\n    <div class='form-group col-sm-6 col-sm-offset-3'>\n        <label for=\"method\">Compter les éléments</label>\n        <select name='method'>\n";
  stack1 = ((helper = (helper = helpers.method_options || (depth0 != null ? depth0.method_options : depth0)) != null ? helper : alias2),(options={"name":"method_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.method_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        </select>\n    </div>\n    </div>\n    </fieldset>\n    <div class=\"form-actions\">\n        <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n        <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n    </div>\n</form>\n</div>\n";
},"useData":true});
templates['criterion.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function";

  return "<td>\n"
    + ((stack1 = ((helper = (helper = helpers.model_label || (depth0 != null ? depth0.model_label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"model_label","hash":{},"data":data}) : helper))) != null ? stack1 : "")
    + "\n</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm' href='#"
    + container.escapeExpression(((helper = (helper = helpers.edit_url || (depth0 != null ? depth0.edit_url : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"edit_url","hash":{},"data":data}) : helper)))
    + "' title=\"Modifier cette entrée\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <a class='btn btn-danger btn-default btn-sm remove' title='Supprimer cette entrée'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n</td>\n";
},"useData":true});
templates['criterion_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Critères composant notre entrée statistique\n<a class='btn btn-primary add' style='font-size: 10px'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n<a class='btn btn-primary add-or' style='font-size: 10px'>Ajouter une clause 'OU' <i class='glyphicon glyphicon-plus'></i></a>\n<a class='btn btn-primary add-and' style='font-size: 10px'>Ajouter une clause 'ET' <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<table class=\"table table-bordered table-condensed table-striped\">\n    <thead>\n        <th class='col-xs-9'>Intitulé</th>\n        <th class='col-xs-3 actions'>Actions</th>\n    </thead>\n    <tbody>\n    </tbody>\n</table>\n";
},"useData":true});
templates['criterion_type_select.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "    <option data-type='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' value='"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "'>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, buffer = 
  "<form >\n    <div class=\"form-group\">\n    <label for='type_id'>Champs de gestion sociale</label>\n    <div class='controls'>\n    <select>\n";
  stack1 = ((helper = (helper = helpers.columns || (depth0 != null ? depth0.columns : depth0)) != null ? helper : helpers.helperMissing),(options={"name":"columns","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),options) : helper));
  if (!helpers.columns) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "    </select>\n    <span class='help-block'>Le champ sur lequel ce critère statistique va porter</span>\n    </div>\n    </div>\n    <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n    <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n</form>\n";
},"useData":true});
templates['datecriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "            <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<div class='well'>\n<form name='criterion'>\n<button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <input type='hidden' name='key' value='"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset><legend>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</legend>\n    <div class='row'>\n    <div class='form-group col-sm-4'>\n        <label for=\"method\">Compter les éléments</label>\n        <select name='method'>\n";
  stack1 = ((helper = (helper = helpers.method_options || (depth0 != null ? depth0.method_options : depth0)) != null ? helper : alias2),(options={"name":"method_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.method_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        </select>\n    </div>\n    <div class=\"form-group col-sm-4\">\n        <label  for='altdate1'>Date 1</label>\n        <input class=\"form-control\" name=\"altdate1\" type=\"text\" autocomplete=\"off\">\n        <input class=\"form-control\" name=\"search1\" type=\"hidden\">\n    </div>\n    <div class=\"form-group col-sm-4\">\n        <label  for='altdate'>Date 2</label>\n        <input class=\"form-control\" name=\"altdate2\" type=\"text\" autocomplete=\"off\">\n        <input class=\"form-control\" name=\"search2\" type=\"hidden\">\n    </div>\n    </div>\n    </fieldset>\n    <div class=\"form-actions\">\n        <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n        <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n    </div>\n</form>\n</div>\n";
},"useData":true});
templates['entry.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<td>\n"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "\n</td>\n<td class='action'>\n    <div class=\"btn-group\">\n        <a class='btn btn-success btn-default btn-sm' href='#entries/"
    + alias4(((helper = (helper = helpers.id || (depth0 != null ? depth0.id : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"id","hash":{},"data":data}) : helper)))
    + "/edit' title=\"Modifier cette entrée\">\n            <i class='glyphicon glyphicon-pencil'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Modifier\n            </span>\n        </a>\n        <button class='btn btn-default btn-sm csv_export' title='Exporter les éléments correspondant à cette entrée statistiques'>\n            <i class='glyphicon glyphicon-export'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Exporter\n            </span>\n        </button>\n        <a class='btn btn-default btn-danger btn-sm remove' title='Supprimer cette entrée'>\n            <i class='glyphicon glyphicon-trash'></i>\n            <span class='visible-lg-inline-block hidden-sm'>\n                Supprimer\n            </span>\n        </a>\n    </div>\n</td>\n";
},"useData":true});
templates['entry_form.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<form >\n<button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <div class=\"form-group\">\n        <label class='control-label' for=\"title\">Intitulé de l'entrée statistique <b class='required'>*</b></label>\n        <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n    </div>\n    <div class=\"form-group\">\n        <label class='control-label' for=\"title\">Description de l'entrée statistique</label>\n        <textarea name='description' class=\"form-control\" id=\"title\" placeholder=\"Description\">"
    + alias4(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n    </div>\n    <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n    <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n</form>\n";
},"useData":true});
templates['entry_list.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h4>Entrées statistiques\n<a class='btn btn-primary' style='font-size: 10px' href='#entries/add'>Ajouter <i class='glyphicon glyphicon-plus'></i></a>\n</h4>\n<div class=\"panel panel-default\">\n    <table class=\"table table-bordered table-condensed table-striped\">\n        <thead>\n            <th class='col-xs-9'>Intitulé</th>\n            <th class='col-xs-3 actions'>Actions</th>\n        </thead>\n        <tbody>\n        </tbody>\n    </table>\n</div>\n";
},"useData":true});
templates['full_entry_form.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<div class='form panel' style='margin-top: 30px; border: 1px solid #9caab9; box-shadow: 0px 0px 4px 0px rgba(6,0,38,0.3);'>\n    <div class='panel-body' style='padding-top: 10px'>\n        <div id='entry_list_header'>\n            <button type='button' class='back-btn btn btn-default'><i class=\"fa fa-close\"></i>&nbsp;Fermer</button>\n            <hr />\n            <div class='row'>\n                <div class='col-xs-9'>\n                    <h4>\n                        Entrée statistique <span><i>"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "</i>&nbsp;</span>\n                    </h4>\n                    <span class='help-block'>"
    + alias4(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"description","hash":{},"data":data}) : helper)))
    + "</span>\n                </div>\n                <div class='col-xs-3'>\n                    <div class='btn-group'>\n                        <button class='btn btn-default edit' title=\"Éditer le titre de l'entrée statistique\">\n                        <i class=\"glyphicon glyphicon-pencil\" style=\"vertical-align:middle\"> </i> Modifier\n                        </button>\n                        <button class='btn btn-default csv_export' title='Exporter les éléments correspondant à cette entrée statistiques'>\n                            <i class='glyphicon glyphicon-export'></i>\n                            Exporter\n                        </button>\n                    </div>\n                </div>\n            </div>\n            <hr />\n            <form id='entry_edit_form' style='display:none' class='well'>\n                <button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n                <fieldset><legend>Édition</legend>\n                <div class='row'>\n                <div class=\"form-group col-xs-6\">\n                    <label class='control-label' for=\"title\">Intitulé de l'entrée statistique <b class='required'>*</b></label>\n                    <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + alias4(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n                    <span class='help-block'>\n                        Sera utilisé dans le fichier de sortie\n                    </span>\n                </div>\n                <div class=\"form-group col-xs-6\">\n                    <label class='control-label' for=\"title\">Description de l'entrée statistique</label>\n                    <textarea name='description' class=\"form-control\" id=\"title\" placeholder=\"Description\">"
    + alias4(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"description","hash":{},"data":data}) : helper)))
    + "</textarea>\n                </div>\n                </div>\n                </fieldset>\n                <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n                <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n            </form>\n\n        </div>\n        <div id='criterion-form'></div>\n        <div id='criteria'></div>\n    </div>\n</div>\n";
},"useData":true});
templates['numbercriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "            <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<div class='well'>\n<form name='criterion'>\n<button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <input type='hidden' name='key' value='"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset><legend>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</legend>\n    <div class='row'>\n    <div class='form-group col-sm-4'>\n        <label for=\"method\">Compter les éléments</label>\n        <select name='method'>\n";
  stack1 = ((helper = (helper = helpers.method_options || (depth0 != null ? depth0.method_options : depth0)) != null ? helper : alias2),(options={"name":"method_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.method_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        </select>\n    </div>\n    <div class=\"form-group col-sm-4\">\n        <label  for='search1'>Valeur 1</label>\n        <input class=\"form-control\" name=\"search1\" type=\"text\" value=\""
    + alias4(((helper = (helper = helpers.search1 || (depth0 != null ? depth0.search1 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"search1","hash":{},"data":data}) : helper)))
    + "\"/>\n    </div>\n    <div class=\"form-group col-sm-4\">\n        <label  for='search2'>Valeur 2</label>\n        <input class=\"form-control\" name=\"search2\" type=\"text\" value=\""
    + alias4(((helper = (helper = helpers.search2 || (depth0 != null ? depth0.search2 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"search2","hash":{},"data":data}) : helper)))
    + "\"/>\n    </div>\n    </div>\n    </fieldset>\n    <div class=\"form-actions\">\n        <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n        <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n    </div>\n</form>\n</div>\n";
},"useData":true});
templates['optrelcriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, alias5=helpers.blockHelperMissing, buffer = 
  "<div class='well'>\n<form name='criterion'>\n<button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <input type='hidden' name='key' value='"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset><legend>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</legend>\n    <div class='row'>\n        <div class='form-group col-sm-6'>\n            <label for=\"method\">Compter les éléments</label>\n            <select name='method' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.method_options || (depth0 != null ? depth0.method_options : depth0)) != null ? helper : alias2),(options={"name":"method_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.method_options) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  buffer += "            </select>\n        </div>\n        <div class=\"form-group col-sm-6\">\n            <label  for='searches'>Parmi</label>\n            <select multiple name='searches' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.optrel_options || (depth0 != null ? depth0.optrel_options : depth0)) != null ? helper : alias2),(options={"name":"optrel_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.optrel_options) { stack1 = alias5.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "            </select>\n        </div>\n    </div>\n    </fieldset>\n    <div class=\"form-actions\">\n        <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n        <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n    </div>\n</form>\n</div>\n";
},"useData":true});
templates['orcriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "                    <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<div class='well'>\n<form name='criterion'>\n    <button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset>\n        <legend>\n            "
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "\n        </legend>\n        <div class='alert alert-info'>\n            <ul>\n            <li>1- Configurer vos critères</li>\n            <li>2- Créer une clause 'OU'</li>\n            <li>3- Sélectionner les critères à utiliser dans la clause 'OU'</li>\n            </ul>\n        </div>\n        <div class='row'>\n            <div class=\"form-group col-sm-6\">\n                <label for=\"criteria\">Combiner les critères</label>\n                <select multiple name='criteria' class='form-control'>\n";
  stack1 = ((helper = (helper = helpers.criteria_options || (depth0 != null ? depth0.criteria_options : depth0)) != null ? helper : alias2),(options={"name":"criteria_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.criteria_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "                </select>\n            </div>\n        </div>\n        <div class=\"form-actions\">\n            <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n            <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n        </div>\n    </fieldset>\n</form>\n</div>\n";
},"useData":true});
templates['sheet_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var helper;

  return "<h3>\n    "
    + container.escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"title","hash":{},"data":data}) : helper)))
    + "\n    <button class='btn btn-default btn-xs edit' style='font-size:9px' title=\"Éditer le titre de la feuille de statistiques\">\n    <i class=\"glyphicon glyphicon-pencil\" style=\"vertical-align:middle\"> </i>\n    </button>\n</h3>\n";
},"3":function(container,depth0,helpers,partials,data) {
    var helper;

  return "<a class='btn btn-default btn-sm' href='"
    + container.escapeExpression(((helper = (helper = helpers.csv_url || (depth0 != null ? depth0.csv_url : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : (container.nullContext || {}),{"name":"csv_url","hash":{},"data":data}) : helper)))
    + "' title='Générer la feuille de statistiques'>\n    <i class='glyphicon glyphicon-file'></i>\n    Générer la sortie csv pour cette feuille de statistiques\n</a>\n";
},"5":function(container,depth0,helpers,partials,data) {
    return "    style='display:none'\n";
},"7":function(container,depth0,helpers,partials,data) {
    return "        Modifier\n";
},"9":function(container,depth0,helpers,partials,data) {
    return "        Ajouter\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {});

  return ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.title : depth0),{"name":"if","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.csv_url : depth0),{"name":"if","hash":{},"fn":container.program(3, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "<form class=\"form-inline\"\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.title : depth0),{"name":"if","hash":{},"fn":container.program(5, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + ">\n  <div class=\"form-group\">\n    <label class='control-label' for=\"title\">Intitulé de la feuille de statistique</label>\n    <input type=\"text\" name='title' class=\"form-control\" id=\"title\" placeholder=\"Titre\" value='"
    + container.escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(alias1,{"name":"title","hash":{},"data":data}) : helper)))
    + "'>\n  </div>\n    <button class=\"btn btn-primary submit\" type=\"submit\">\n"
    + ((stack1 = helpers["if"].call(alias1,(depth0 != null ? depth0.title : depth0),{"name":"if","hash":{},"fn":container.program(7, data, 0),"inverse":container.program(9, data, 0),"data":data})) != null ? stack1 : "")
    + "    </button>\n</form>\n";
},"useData":true});
templates['stringcriterion_form.mustache'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "            <option value='"
    + alias4(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"value","hash":{},"data":data}) : helper)))
    + "' ";
  stack1 = ((helper = (helper = helpers.selected || (depth0 != null ? depth0.selected : depth0)) != null ? helper : alias2),(options={"name":"selected","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.selected) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + ">"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</option>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "selected";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, options, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression, buffer = 
  "<div class='well'>\n<form name='criterion'>\n<button type=\"button\" class=\"close\"><span aria-hidden=\"true\">&times;</span></button>\n    <input type='hidden' name='type' value='"
    + alias4(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"type","hash":{},"data":data}) : helper)))
    + "' />\n    <input type='hidden' name='key' value='"
    + alias4(((helper = (helper = helpers.key || (depth0 != null ? depth0.key : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"key","hash":{},"data":data}) : helper)))
    + "' />\n    <fieldset><legend>"
    + alias4(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"label","hash":{},"data":data}) : helper)))
    + "</legend>\n    <div class='row'>\n    <div class='form-group col-sm-4'>\n        <label for=\"method\">Compter les éléments</label>\n        <select name='method'>\n";
  stack1 = ((helper = (helper = helpers.method_options || (depth0 != null ? depth0.method_options : depth0)) != null ? helper : alias2),(options={"name":"method_options","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data}),(typeof helper === alias3 ? helper.call(alias1,options) : helper));
  if (!helpers.method_options) { stack1 = helpers.blockHelperMissing.call(depth0,stack1,options)}
  if (stack1 != null) { buffer += stack1; }
  return buffer + "        </select>\n    </div>\n    <div class=\"form-group col-sm-4\">\n        <label  for='search1'>Valeur</label>\n        <input class=\"form-control\" name=\"search1\" type=\"text\" value=\""
    + alias4(((helper = (helper = helpers.search1 || (depth0 != null ? depth0.search1 : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"search1","hash":{},"data":data}) : helper)))
    + "\"/>\n    </div>\n    </div>\n    </fieldset>\n    <div class=\"form-actions\">\n        <button type=\"submit\" class=\"btn btn-success\" name='submit'>Valider</button>\n        <button type=\"reset\" class=\"btn btn-danger\" name=\"cancel\">Annuler</button>\n    </div>\n</form>\n</div>\n";
},"useData":true});
})();