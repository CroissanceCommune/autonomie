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
    #messageboxes{
        position:fixed;
        bottom:0px;
        left:50px;
        z-index:2000;
    }
    table thead th{
        background-color:#D9EDF7;
    }
    table tfoot td{
        background-color:#FCF8E3;
    }
</style>
<br />
${period_form.render()|n}
<hr />
% if edit:
    <a href="#lines/add" class='btn btn-large visible-tablet hidden-desktop' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais</a>
    <a href="#kmlines/add" class='btn btn-large visible-tablet hidden-desktop' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais kilométriques</a>
% endif
<div class='row'>
    <div class='span12' id="expenses"></div>
    <div class='span12' id="expenseskm"></div>
    <div id="form-container" class='span4'></div>
</div>
<hr />
<p class='lead' id='total' style='text-align:right'></p>
% if edit:
<hr />
    ${form|n}
% else:
<div class='well'>
    ${api.format_expense_status(request.context)}<br />
    % if request.context.comments :
        <blockquote>
            ${request.context.comments|n}
        </blockquote>
    % endif
</div>
% endif
<div id='messageboxes'>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
% if edit:
    AppOptions['edit'] = true;
% else:
    AppOptions['edit'] = false;
% endif
</%block>
