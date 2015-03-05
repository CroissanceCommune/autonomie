(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['holidayForm.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<form id='holidayForm' class='form' action='#' onsubmit='return false;'>\n<div class=\"form-group\">\n<label class=\"control-label\" for='alt_start_date'>Début</label>\n<div class='controls'>\n    <input name=\"alt_start_date\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n    <input name=\"start_date\" type=\"hidden\">\n</div>\n</div>\n<div class=\"form-group\">\n<label class=\"control-label\" for='alt_end_date'>Fin</label>\n<div class='controls'>\n    <input name=\"alt_end_date\" class=\"input-small\" type=\"text\" autocomplete=\"off\">\n    <input name=\"end_date\" type=\"hidden\">\n</div>\n</div>\n\n<div class=\"form-actions\">\n<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>\n<button type=\"reset\" class=\"btn btn-default\" name=\"cancel\">Annuler</button>\n</div>\n</form>\n";
  },"useData":true});
templates['holidayList.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<div>\n    <table class=\"opa table table-bordered table-condensed\">\n        <caption>\n        Vos congés\n            <div class=\"inline-element\">\n                <a class='btn btn-info add' title=\"Déclarer un congés\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n            </div>\n        </caption>\n        <thead>\n            <th>Date de début</th>\n            <th>Date de fin</th>\n            <th>Actions</th>\n        </thead>\n        <tbody>\n        </tbody>\n    </table>\n</div>\n";
  },"useData":true});
templates['holiday.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
  return "<td>"
    + escapeExpression(((helper = (helper = helpers.alt_start_date || (depth0 != null ? depth0.alt_start_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"alt_start_date","hash":{},"data":data}) : helper)))
    + "</td>\n<td>"
    + escapeExpression(((helper = (helper = helpers.alt_end_date || (depth0 != null ? depth0.alt_end_date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"alt_end_date","hash":{},"data":data}) : helper)))
    + "</td>\n<td><a class='btn btn-default edit'><i class='icon icon-pencil'></i>&nbsp;Éditer</a><a class='btn btn-default remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</a></td>\n";
},"useData":true});
})();