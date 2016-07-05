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
<a class='btn btn-default pull-right' href='#print'><i class='glyphicon glyphicon-print'></i>Imprimer</a>
<a class='btn btn-default pull-right' href='${request.route_path("expensexlsx", id=expense.id)}' ><i class='glyphicon glyphicon-file'></i>Excel</a>
    </div>
</div>
<br/>
<div class='row well'>
    <div class="col-md-6">
        <div class="hidden-print">
        <i class='glyphicon glyphicon-play'></i>
        <strong>
    % if expense.status == 'resulted':
        Cette feuille de notes de dépense a été intégralement payée.
    % elif expense.status == 'paid':
        Cette feuille de notes de dépense a été partiellement payée.
    % elif expense.status == 'valid':
            Cette feuille de notes de dépense a été validée, elle est en attente de paiement.
    % elif expense.status == 'wait':
            Cette feuille de notes de dépense est en attente de validation
    % elif expense.status == 'draft':
        Cette feuille de notes de dépense est un brouillon
    % elif expense.status == 'invalid':
        Cette feuille de notes de dépense est invalide
    % endif
        </strong>
        <ul>
            <li>
                ${api.format_expense_status(expense)}<br />
            </li>
        % if request.has_permission('admin_treasury'):
            <li>
            L'identifiant de cette feuille de notes de dépense est : <strong>${ expense.id }</strong>
            </li>
            <li>
                % if expense.exported:
                    Ce document a déjà été exporté vers le logiciel de comptabilité
                %else:
                    Ce document n'a pas encore été exporté vers le logiciel de comptabilité
                % endif
            </li>
        % endif
        % if expense.payments:
            <li>
            Paiement(s) recu(s):
            <ul>
                % for payment in expense.payments:
                    <% url = request.route_path('expense_payment', id=payment.id) %>
                    <li>
                    <a href="${url}">
                        ${api.format_amount(payment.amount)|n}&nbsp;€
                        le ${api.format_date(payment.date)}
                        % if payment.waiver:
                            (par abandon de créances)
                        % else:
                            (${api.format_paymentmode(payment.mode)}
                            % if payment.bank:
                                &nbsp;${payment.bank.label}
                            % endif
                            )
                        % endif
                    </a>
                    </li>
                % endfor
            </ul>
            </li>
        % endif

        </ul>
    </div>
    <div class="hidden-print">
        <i class='glyphicon glyphicon-play'></i>
        <strong>Justificatifs</strong>
        <br />
        ${format_filelist(expense)}
        % if not expense.children:
            <small>
                Aucun justificatif n'a été déposé
            </small>
        % endif
    </div>
</div>
<div class="col-md-6">
    <div class="hidden-print">
    % for com in communication_history:
        % if loop.first:
            <div class="">
                <i class='glyphicon glyphicon-play'></i>
                <strong>Historique des Communications Entrepreneurs-CAE</strong>
        % endif
        % if com.content.strip():
            <blockquote>
                <p style="font-size: 14px">
                ${format_text(com.content)}
            </p>
            <footer>${api.format_account(com.user)} le ${api.format_date(com.date)}</footer>
            </blockquote>
        % endif
        % if loop.last:
            </div>
        % endif
    % endfor
    </div>
</div>
</div>
<hr />
<div class='row'>
    <div class='col-md-12' id="expenses"></div>
</div>
<div class='row'>
    <div class='col-md-12' id="expenseskm"></div>
    <div id="form-container"></div>
</div>
<hr />
<p class='lead' id='total' style='text-align:right'></p>
<hr />
    ${form|n}
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
