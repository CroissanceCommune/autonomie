<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>

<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_text" />
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
<a class='btn pull-right' href='${request.route_path("expensexlsx", id=request.context.id)}' ><i class='icon-file'></i>Export</a>
${period_form.render()|n}
<hr />
% if request.context.status == 'resulted':
    <div class="well hidden-print">
        <span class="label label-important"><i class='icon-white icon-play'></i></span>
        Cette note de frais a été payée.
    </div>
% elif request.context.status == 'valid':
    <div class="well hidden-print">
        <span class="label label-important"><i class='icon-white icon-play'></i></span>
        Cette note de frais a été validée, elle est en attente de paiement.
    </div>
% elif request.context.status == 'wait':
    <div class="well hidden-print">
        <span class="label label-important"><i class='icon-white icon-play'></i></span>
        Cette note de frais est en attente de validation
    </div>
% endif
<div class="row hidden-print">
% for com in communication_history:
    % if loop.first:
        <div class="well">
            <b>Historique des Communications Entrepreneurs-CAE</b>
    % endif
        <hr />
        <p class="font-size:10px;">
            ${format_text(com.content)}
        </p>
        <small>${api.format_account(com.user)} le ${api.format_date(com.date)}</small>
    % if loop.last:
        </div>
    % endif
% endfor
</div>
% if edit:
    <div class="hidden-print">
    <a href="#lines/add" class='btn btn-large visible-tablet hidden-desktop' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais</a>
    <a href="#kmlines/add" class='btn btn-large visible-tablet hidden-desktop' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais kilométriques</a>
    <a href="#tel/add" class='btn btn-large visible-tablet hidden-desktop' title="Ajouter une ligne"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des frais téléphoniques</a>
</div>
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
