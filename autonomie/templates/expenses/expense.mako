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

<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name="headtitle">
${request.layout_manager.render_panel('task_title_panel', title=title)}
</%block>
<%block name="beforecontent">
<% expense = request.context %>
<br />
<div class='container-fluid'>
    <div class="row">
        <div id="header-container" class="text-right">
            <button class='btn btn-default' onclick="window.print()"><i class='glyphicon glyphicon-print'></i> Imprimer</button>
            <a class='btn btn-default' href='${request.route_path("/expenses/{id}.xlsx", id=expense.id)}' ><i class='glyphicon glyphicon-file'></i> Excel</a>
        </div>
    </div>
    <div class='row well'>
        <div class="col-md-6">
            <div class="hidden-print">
                <i class='glyphicon glyphicon-play'></i>
                <strong>
            % if expense.paid_status == 'resulted':
                Cette feuille de notes de dépense a été intégralement payée.
            % elif expense.paid_status == 'paid':
                Cette feuille de notes de dépense a été partiellement payée.
            % elif expense.status == 'valid':
                    Cette feuille de notes de dépense a été validée, elle est en attente de paiement.
            % elif expense.status == 'wait':
                    Cette feuille de notes de dépense est en attente de validation.
            % elif expense.status == 'draft':
                Cette feuille de notes de dépense est un brouillon.
            % elif expense.status == 'invalid':
                Cette feuille de notes de dépense est invalide.
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
                                Par ${api.format_account(payment.user)} :&nbsp;
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
                <a
                    href="${request.route_path('/expenses/{id}/addfile', id=expense.id)}"
                    class="btn btn-primary secondary-action">
                    <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Ajouter un fichier
                </a>
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
</div>
</%block>
<%block name='content'>
<div id="js-main-area"></div>
</%block>
<%block name='footer'>
<script type='text/javascript'>
var AppOption = {};
AppOption['context_url'] = "${context_url}";
AppOption['form_config_url'] = "${form_config_url}"
% if request.has_permission("edit.expensesheet"):
    AppOption['edit'] = true;
% else:
    AppOption['edit'] = false;
% endif
</script>
</%block>
