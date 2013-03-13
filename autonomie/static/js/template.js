var templates = {};
templates.expenseadsl = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<td colspan='3'>Tel fixe + Adsl</td>");_.b("\n" + i);_.b("<td><input type='text' class='input-small' value='");_.b(_.v(_.f("ht",c,p,0)));_.b("' name='ht'/></td>");_.b("\n" + i);_.b("<td><input type='text' class='input-small' value='");_.b(_.v(_.f("tva",c,p,0)));_.b("' name='tva'/></td>");_.b("\n" + i);_.b("<td>");_.b(_.t(_.f("total",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td></td>");return _.fl();;});
templates.expenseForm = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<form id='expenseForm' class='form' action='#' onsubmit='return false;'>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='category'>Catégorie de frais</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);if(_.s(_.f("category_options",c,p,1),c,p,0,218,349,"{{ }}")){_.rs(c,p,function(c,p,_){_.b("<label class=\"radio\">");_.b("\n" + i);_.b("<input type='radio' name='category' value='");_.b(_.v(_.f("value",c,p,0)));_.b("' ");if(_.s(_.f("selected",c,p,1),c,p,0,308,315,"{{ }}")){_.rs(c,p,function(c,p,_){_.b("checked");});c.pop();}_.b("> ");_.b(_.v(_.f("label",c,p,0)));_.b("\n" + i);_.b("</label>");_.b("\n");});c.pop();}_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='code'>Type de frais</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<select class='input-xlarge' name='code'>");_.b("\n" + i);if(_.s(_.f("type_options",c,p,1),c,p,0,560,648,"{{ }}")){_.rs(c,p,function(c,p,_){_.b("<option value='");_.b(_.v(_.f("value",c,p,0)));_.b("' ");if(_.s(_.f("selected",c,p,1),c,p,0,600,615,"{{ }}")){_.rs(c,p,function(c,p,_){_.b("selected='true'");});c.pop();}_.b(">");_.b(_.v(_.f("label",c,p,0)));_.b("</option>");_.b("\n");});c.pop();}_.b("</select>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='altdate'>Date</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<input name=\"altdate\" class=\"input-small\" type=\"text\">");_.b("\n" + i);_.b("<input name=\"date\" class=\"input-small\" type=\"hidden\">");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='description'>Description</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<input type='text' class='input-xlarge' name='description' value='");_.b(_.v(_.f("description",c,p,0)));_.b("'/>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='ht'>Montant HT</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<div class=\"input-append\">");_.b("\n" + i);_.b("    <input type='text' class='input-small' name='ht' value='");_.b(_.v(_.f("ht",c,p,0)));_.b("' /><span class=\"add-on\">&euro;</span>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='tva'>Montant de la Tva</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<div class=\"input-append\">");_.b("\n" + i);_.b("<input type='text' class='input-small' name='tva' value='");_.b(_.v(_.f("tva",c,p,0)));_.b("' /><span class=\"add-on\">&euro;</span>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"form-actions\">");_.b("\n" + i);_.b("<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>");_.b("\n" + i);_.b("<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</form>");return _.fl();;});
templates.expenseKmForm = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<form id='expenseKmForm' class='form' action='#' onsubmit='return false;'>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);if(_.s(_.f("type_options",c,p,1),c,p,0,144,271,"{{ }}")){_.rs(c,p,function(c,p,_){_.b("<label class=\"radio\">");_.b("\n" + i);_.b("<input type='radio' name='type' value='");_.b(_.v(_.f("value",c,p,0)));_.b("' ");if(_.s(_.f("selected",c,p,1),c,p,0,230,237,"{{ }}")){_.rs(c,p,function(c,p,_){_.b("checked");});c.pop();}_.b("> ");_.b(_.v(_.f("label",c,p,0)));_.b("\n" + i);_.b("</label>");_.b("\n");});c.pop();}_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='altdate'>Date</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<input name=\"altdate\" class=\"input-small\" type=\"text\">");_.b("\n" + i);_.b("<input name=\"date\" class=\"input-small\" type=\"hidden\">");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='start'>Point de départ</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<input type='text' class='input-medium' name='start' value='");_.b(_.v(_.f("start",c,p,0)));_.b("'/>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='end'>Point d'arrivée</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<input type='text' class='input-medium' name='end' value='");_.b(_.v(_.f("end",c,p,0)));_.b("'/>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"control-group\">");_.b("\n" + i);_.b("<label class=\"control-label\" for='ht'>Nombre de Kilomètres</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<div class=\"input-append\">");_.b("\n" + i);_.b("    <input type='text' class='input-small' name='km' value='");_.b(_.v(_.f("km",c,p,0)));_.b("' /><span class=\"add-on\">km</span>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class='control-group'>");_.b("\n" + i);_.b("<label class=\"control-label\" for='description'>Prestation</label>");_.b("\n" + i);_.b("<div class='controls'>");_.b("\n" + i);_.b("<input type='text' class='input-xlarge' name='description' value='");_.b(_.v(_.f("description",c,p,0)));_.b("' />");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("\n" + i);_.b("<div class=\"form-actions\">");_.b("\n" + i);_.b("<button type=\"submit\" class=\"btn btn-primary\" name='submit'>Valider</button>");_.b("\n" + i);_.b("<button type=\"reset\" class=\"btn\" name=\"cancel\">Annuler</button>");_.b("\n" + i);_.b("</div>");_.b("\n" + i);_.b("</form>");return _.fl();;});
templates.expenseKmList = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<table class=\"table table-striped table-bordered table-condensed\">");_.b("\n" + i);_.b("    <caption>Frais kilométriques</caption>");_.b("\n" + i);_.b("    <thead>");_.b("\n" + i);_.b("        <th>Date</th>");_.b("\n" + i);_.b("        <th>Type</th>");_.b("\n" + i);_.b("        <th class='span3'>Prestation</th>");_.b("\n" + i);_.b("        <th>Point de départ</th>");_.b("\n" + i);_.b("        <th>Point d'arrivée</th>");_.b("\n" + i);_.b("        <th>Kms</th>");_.b("\n" + i);_.b("        <th>Indemnités</th>");_.b("\n" + i);_.b("        <th>Actions</th>");_.b("\n" + i);_.b("    </thead>");_.b("\n" + i);_.b("    <tbody class='internal'>");_.b("\n" + i);_.b("    </tbody>");_.b("\n" + i);_.b("    <tfoot>");_.b("\n" + i);_.b("        <tr>");_.b("\n" + i);_.b("            <td colspan='6'>Total</td>");_.b("\n" + i);_.b("            <td id='km_total'></td>");_.b("\n" + i);_.b("            <td></td>");_.b("\n" + i);_.b("        </tr>");_.b("\n" + i);_.b("    </tfoot>");_.b("\n" + i);_.b("</table>");return _.fl();;});
templates.expenseKm = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<td>");_.b(_.v(_.f("date",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("typelabel",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("description",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("start",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("end",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("km",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.t(_.f("total",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td><a class='btn' href='");_.b(_.v(_.f("edit_url",c,p,0)));_.b("' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>");_.b("\n" + i);_.b("<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</td>");return _.fl();;});
templates.expenseList = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<div>");_.b("\n" + i);_.b("<table class=\"table table-bordered table-condensed table-disable-hover\">");_.b("\n" + i);_.b("    <caption>Frais liés au fonctionnement de l'entreprise</caption>");_.b("\n" + i);_.b("    <thead>");_.b("\n" + i);_.b("        <th class='span3'>Type de frais</th>");_.b("\n" + i);_.b("        <th>Date</th>");_.b("\n" + i);_.b("        <th class='span3'>Description</th>");_.b("\n" + i);_.b("        <th>Montant HT</th>");_.b("\n" + i);_.b("        <th>Tva</th>");_.b("\n" + i);_.b("        <th>Total</th>");_.b("\n" + i);_.b("        <th>Actions</th>");_.b("\n" + i);_.b("    </thead>");_.b("\n" + i);_.b("    <tbody class='internal'>");_.b("\n" + i);_.b("    </tbody>");_.b("\n" + i);_.b("    <tfoot>");_.b("\n" + i);_.b("        <tr>");_.b("\n" + i);_.b("            <td colspan='5'>Total</td>");_.b("\n" + i);_.b("            <td id='internal_total'></td>");_.b("\n" + i);_.b("            <td></td>");_.b("\n" + i);_.b("        </tr>");_.b("\n" + i);_.b("    </tfoot>");_.b("\n" + i);_.b("</table>");_.b("\n" + i);_.b("<br />");_.b("\n" + i);_.b("<table class=\"table table-bordered table-condensed table-disable-hover\">");_.b("\n" + i);_.b("    <caption>Frais liés à l'activité</caption>");_.b("\n" + i);_.b("    <thead>");_.b("\n" + i);_.b("        <th class='span3'>Type de frais</th>");_.b("\n" + i);_.b("        <th>Date</th>");_.b("\n" + i);_.b("        <th class='span3'>Description</th>");_.b("\n" + i);_.b("        <th>Montant HT</th>");_.b("\n" + i);_.b("        <th>Tva</th>");_.b("\n" + i);_.b("        <th>Total</th>");_.b("\n" + i);_.b("        <th>Actions</th>");_.b("\n" + i);_.b("    </thead>");_.b("\n" + i);_.b("    <tbody class='activity'>");_.b("\n" + i);_.b("    </tbody>");_.b("\n" + i);_.b("    <tfoot>");_.b("\n" + i);_.b("        <tr>");_.b("\n" + i);_.b("            <td colspan='5'>Total</td>");_.b("\n" + i);_.b("            <td id='activity_total'></td>");_.b("\n" + i);_.b("            <td></td>");_.b("\n" + i);_.b("        </tr>");_.b("\n" + i);_.b("    </tfoot>");_.b("\n" + i);_.b("</table>");_.b("\n" + i);_.b("</div>");return _.fl();;});
templates.expensemobile = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<td colspan='3'>Tel mobile</td>");_.b("\n" + i);_.b("<td><input type='text' class='input-small' value='");_.b(_.v(_.f("ht",c,p,0)));_.b("' name='ht'/></td>");_.b("\n" + i);_.b("<td><input type='text' class='input-small' value='");_.b(_.v(_.f("tva",c,p,0)));_.b("' name='tva'/></td>");_.b("\n" + i);_.b("<td>");_.b(_.t(_.f("total",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td></td>");return _.fl();;});
templates.expense = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<td>");_.b(_.v(_.f("typelabel",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("altdate",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("description",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("ht",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.v(_.f("tva",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td>");_.b(_.t(_.f("total",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td><a class='btn' href='");_.b(_.v(_.f("edit_url",c,p,0)));_.b("' ><i class='icon icon-pencil'></i>&nbsp;Éditer</a>");_.b("\n" + i);_.b("<a class='btn remove'><i class='icon icon-remove-sign'></i>&nbsp;Supprimer</td>");return _.fl();;});
templates.expensetel = new Hogan.Template(function(c,p,i){var _=this;_.b(i=i||"");_.b("<td colspan='3'>");_.b(_.v(_.f("typelabel",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td><div class='control-group'><div class='controls'><input type='text' class='input-small' value='");_.b(_.v(_.f("ht",c,p,0)));_.b("' name='ht'/></div></div></td>");_.b("\n" + i);_.b("<td><div class='control-group'><div class='controls'><input type='text' class='input-small' value='");_.b(_.v(_.f("tva",c,p,0)));_.b("' name='tva'/></div></div></td>");_.b("\n" + i);_.b("<td>");_.b(_.t(_.f("total",c,p,0)));_.b("</td>");_.b("\n" + i);_.b("<td></td>");return _.fl();;});
