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
<% expense = request.context %>
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
<a class='btn btn-default pull-right' href='${request.route_path("expensexlsx", id=expense.id)}' ><i class='glyphicon glyphicon-file'></i>Export</a>
${period_form.render()|n}
<hr />
    <div class="well hidden-print">
        <span class="label label-important"><i class='glyphicon glyphicon-white icon-play'></i></span>
% if expense.status == 'resulted':
    Cette note de dépense a été intégralement payée.
% elif expense.status == 'paid':
    Cette note de dépense a été partiellement payée.
% elif expense.status == 'valid':
        Cette note de dépense a été validée, elle est en attente de paiement.
% elif expense.status == 'wait':
        Cette note de dépense est en attente de validation
% endif
        <p>
            <small>
                ${api.format_expense_status(expense)}<br />
            </small>
        </p>
        % if expense.payments:
            Paiement(s) recu(s):
            <ul>
                % for payment in expense.payments:
                    <% url = request.route_path('expense_payment', id=payment.id) %>
                    <li>
                    <a href="${url}">
                        ${api.format_amount(payment.amount)|n}&nbsp;€
                        le ${api.format_date(payment.date)}
                        (${api.format_paymentmode(payment.mode)}
                        % if payment.bank:
                            &nbsp;${payment.bank.label}
                        % endif
                        )
                    </a>
                    </li>
                % endfor
            </ul>
        % endif

% if request.has_permission('admin_treasury'):
    <p>
    <small>
        L'identifiant de cette notes de dépense est : ${ expense.id }
    </small>
</p>
<p>
    <small>
        % if expense.exported:
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
    ${format_filelist(expense)}
    % if not expense.children:
        <small>
            Aucun justificatif n'a été déposé
        </small>
    % endif
</div>
<div class="hidden-print">
% for com in communication_history:
    % if loop.first:
        <div class="well">
            <b>Historique des Communications Entrepreneurs-CAE</b>
    % endif
    % if com.content.strip():
        <hr />
        <p>
            ${format_text(com.content)}
        </p>
        <small>${api.format_account(com.user)} le ${api.format_date(com.date)}</small>
    % endif
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
