(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['sheet_form.mustache'] = template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
  return "<form class=\"form-inline\">\n  <div class=\"form-group\">\n    <label for=\"title\">Intitulé de la feuille de statistique</label>\n    <input type=\"text\" class=\"form-control\" id=\"title\" placeholder=\"Titre\">\n  </div>\n  <button type=\"submit\" class=\"btn btn-primary\">Ajouter</button>\n</form>\n";
  },"useData":true});
})();