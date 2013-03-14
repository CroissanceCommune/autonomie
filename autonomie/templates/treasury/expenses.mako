<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
<style>
    #period_form label{
        width:0px;
    }
    #period_form .control-group, #period_form .form-actions{
        float:left;
        display:inline-block;
        padding:5px;
        padding-left:20px;
        margin:3px;
        border:none;
        margin-bottom:10px;
    }
    #period_form .controls{
        margin-left:0px;
    }
</style>
<br />
${period_form.render()|n}

<a href="#lines/add" class='btn btn-large' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>
<a href="#kmlines/add" class='btn btn-large' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais kilométriques</a>
<div class='row'>
    <div class='span12' id="expenses"></div>
    <div class='span12' id="expenseskm"></div>
    <div id="form-container" class='span4'></div>
</div>
${form|n}
</%block>
<%block name="footerjs">
AppOptions = jQuery.parseJSON('${jsoptions|n}');
AppOptions['expensecategories'] = [{'value':'1', 'label':'Frais direct de fonctionnement'}, {'value':'2', 'label':"Frais concernant directement votre l'activite aupres de vos clients"}];
AppOptions['expense'] = jQuery.parseJSON('${expensesheet|n}');
</%block>
