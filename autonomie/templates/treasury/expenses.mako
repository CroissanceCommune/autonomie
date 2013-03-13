<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
${period_form.render()|n}
<a href="#lines/add" class='btn btn-large' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>
<a href="#kmlines/add" class='btn btn-large' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais kilométriques</a>
<div class='row'>
    <div class='span12' id="expenses"></div>
    <div class='span12' id="expenseskm"></div>
    <div id="form-container" class='span4'></div>
</div>
</%block>
<%block name="footerjs">
AppOptions = jQuery.parseJSON('${jsoptions|n}');
AppOptions['expensecategories'] = [{'value':'1', 'label':'Frais direct de fonctionnement'}, {'value':'2', 'label':"Frais concernant directement votre l'activite aupres de vos clients"}];
AppOptions['expense'] = jQuery.parseJSON('${expensesheet|n}');
</%block>
