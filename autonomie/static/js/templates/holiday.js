(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['empty.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<td colspan='3'>Aucun congés n'a été saisi</td>\n";
},"useData":true});
templates['holidayForm.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<form id='holidayForm' class='form' action='#' onsubmit='return false;'>\n<div class=\"form-group\">\n<label class=\"control-label\" for='alt_start_date'>Début</label>\n<div class='controls'>\n    <input name=\"alt_start_date\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n    <input name=\"start_date\" type=\"hidden\">\n</div>\n</div>\n<div class=\"form-group\">\n<label class=\"control-label\" for='alt_end_date'>Fin</label>\n<div class='controls'>\n    <input name=\"alt_end_date\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n    <input name=\"end_date\" type=\"hidden\">\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn btn-default\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
},"useData":true});
templates['holidayList.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<div class='panel panel-default page-block'>\n    <div class='panel-heading'>\n        Vos congés\n    </div>\n    <div class='panel-body'>\n        <a class='btn btn-primary primary-action' title=\"Déclarer un congés\">\n            <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Ajouter\n            </a>\n        <table class=\"opa table table-bordered table-condensed\">\n            <thead>\n                <th>Date de début</th>\n                <th>Date de fin</th>\n                <th>Actions</th>\n            </thead>\n            <tbody>\n            </tbody>\n        </table>\n    </div>\n</div>\n";
},"useData":true});
templates['holiday.mustache'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper, alias1=depth0 != null ? depth0 : (container.nullContext || {}), alias2=helpers.helperMissing, alias3="function", alias4=container.escapeExpression;

  return "<td>"
    + alias4(((helper = (helper = helpers.alt_start_date || (depth0 != null ? depth0.alt_start_date : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"alt_start_date","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + alias4(((helper = (helper = helpers.alt_end_date || (depth0 != null ? depth0.alt_end_date : depth0)) != null ? helper : alias2),(typeof helper === alias3 ? helper.call(alias1,{"name":"alt_end_date","hash":{},"data":data}) : helper)))
    + "</td>\n<td><a class='btn btn-default edit'><i class='glyphicon glyphicon-pencil'></i>&nbsp;Éditer</a><a class='btn btn-default remove'><i class='glyphicon glyphicon-remove-sign'></i>&nbsp;Supprimer</a></td>\n";
},"useData":true});
})();