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
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name="content">
<style>
    #period_form label{
        width:0px;
    }
    #period_form .form-group, #period_form .form-actions{
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
<div class="row">
    <div id="header-container">
    </div>
</div>
<a class='btn btn-default pull-right' href='#print'><i class='glyphicon glyphicon-print'></i>Imprimer</a>
<a class='btn btn-default pull-right' href='${request.route_path("expensexlsx", id=request.context.id)}' ><i class='glyphicon glyphicon-file'></i>Export</a>
${period_form.render()|n}
<hr />
    <div class="well hidden-print">
        <span class="label label-important"><i class='glyphicon glyphicon-white icon-play'></i></span>
% if request.context.status == 'resulted':
        Cette note de frais a été payée.
% elif request.context.status == 'valid':
        Cette note de frais a été validée, elle est en attente de paiement.
% elif request.context.status == 'wait':
        Cette note de frais est en attente de validation
% endif
        <p>
            <small>
                ${api.format_expense_status(request.context)}<br />
            </small>
        </p>
% if request.user.is_admin():
    <p>
    <small>
        L'identifiant de cette notes de frais est : ${ request.context.id }
    </small>
</p>
<p>
    <small>
        % if request.context.exported:
            Ce document a déjà été exporté vers le logiciel de comptabilité
        %else:
            Ce document n'a pas encore été exporté vers le logiciel de comptabilité
        % endif
    </small>
</p>
% endif
</div>
<div class="well hidden-print">
    <h5>Justificatifs</h5>
    ${format_filelist(request.context)}
    % if not request.context.children:
        <small>
            Aucun justificatif n'a été déposé
        </small>
    % endif
</div>
<div class="row hidden-print">
% for com in communication_history:
    % if loop.first:
        <div class="well">
            <b>Historique des Communications Entrepreneurs-CAE</b>
    % endif
        <hr />
        <p>
            ${format_text(com.content)}
        </p>
        <small>${api.format_account(com.user)} le ${api.format_date(com.date)}</small>
    % if loop.last:
        </div>
    % endif
% endfor
</div>
<div class='row'>
    <div class='col-md-12' id="expenses"></div>
</div>
<div class='row'>
    <div class='col-md-12' id="expenseskm"></div>
    <div id="form-container"></div>
</div>
<hr />
<p class='lead' id='total' style='text-align:right'></p>
% if edit:
<hr />
    ${form|n}
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
