<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
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
<%doc>
Admin expenses list view
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    <a href='#filter-form'
        data-toggle='collapse'
        aria-expanded="false"
        aria-controls="filter-form">
        <i class='glyphicon glyphicon-search'></i>&nbsp;
        Filtres&nbsp;
        <i class='glyphicon glyphicon-chevron-down'></i>
    </a>
    % if '__formid__' in request.GET:
        <div class='help-text'>
            <small><i>Des filtres sont actifs</i></small>
        </div>
        <div class='help-text'>
            <a href="${request.current_route_path(_query={})}">
                <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
            </a>
        </div>
    % endif
    </div>
    <div class='panel-body'>
    % if '__formid__' in request.GET:
        <div class='collapse' id='filter-form'>
    % else:
        <div class='in collapse' id='filter-form'>
    % endif
            <div class='row'>
                <div class='col-xs-12'>
                    ${form|n}
                </div>
            </div>
        </div>
    </div>
</div>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    ${records.item_count} Résultat(s)
    </div>
    <div class='panel-body'>
    <div class='row'>
        <div class='col-md-4 col-xs-12'>
        ${request.layout_manager.render_panel('list_legend', legends=legends)}
        </div>
    </div>
<table class="table table-condensed table-bordered status-table">
    <thead>
        <tr>
        <th></th>
            <th>${sortable(u"Identifiant", "id_")}</th>
            <th> ${sortable(u"Entrepreneur", "name")}</th>
            <th>${sortable(u"Période", "month")}</th>
            <th>Montant</th>
            <th>Paiements</th>
            <th>Justificatifs</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % for expense in records:
            <% url = request.route_path('/expenses/{id}', id=expense.id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <tr class="status status-${expense.status} paid-status-${expense.paid_status} justified-${expense.justified}">
                <td class='status-td'>
                    <br />
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${expense.id}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(expense.user)} ( ${expense.company.name} )
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.month_name(expense.month)} - ${expense.year}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_amount(expense.total, trim=True)|n}&nbsp;&euro;
                </td>
                <td onclick="${onclick}" class="rowlink">
                    % for payment in expense.payments:
                        % if loop.first:
                            <ul>
                        % endif
                                <% url = request.route_path('expense_payment', id=payment.id) %>
                                <li>
                                <a href="${url}">
                                    Par ${api.format_account(payment.user)} :
                                    ${api.format_amount(payment.amount)|n}&nbsp;€
                                    le ${api.format_date(payment.date)}
                                    % if payment.waiver:
                                        (par abandon de créances)
                                    % else:
                                        (${api.format_paymentmode(payment.mode)})
                                    % endif
                                </a>
                                </li>
                        % if loop.last:
                            </ul>
                        % endif
                    % endfor
                </td>
                <td>
                    % if api.has_permission('set_justified.expensesheet', expense) and expense.status != 'valid':
                    <div
                        class="btn-group expense-justify"
                        data-toggle="buttons"
                        data-href="${request.route_path('/api/v1/expenses/{id}', id=expense.id, _query={'action': 'justified_status'})}"
                        >
                        <label
                            class="btn btn-default
                            % if not expense.justified:
                            active
                            % endif
                            ">
                            <input
                                name=""
                                value="false"
                                % if not expense.justified:
                                checked="true"
                                % endif
                                autocomplete="off"
                                type="radio">
                                <i class="fa fa-clock-o"></i> En attente
                        </label>
                        <label
                            class="btn btn-default
                            % if expense.justified:
                            active
                            % endif
                            ">
                            <input
                            name=""
                            value="true"
                            autocomplete="off"
                                % if expense.justified:
                                checked="true"
                                % endif
                            type="radio">
                            <i class="fa fa-check"></i> Reçus
                        </label>
                    </div>
                    % endif
                </td>
                <td>
                    <% url = request.route_path('/expenses/{id}', id=expense.id) %>
                    ${table_btn(url, u'Modifier', u"Voir la note de dépense", icon="pencil" )}
                    <% url = request.route_path('/expenses/{id}.xlsx', id=expense.id) %>
                    ${table_btn(url, u'Excel', u"Télécharger au format Excel", icon="file" )}
                    % if request.has_permission('add_payment.expensesheet', expense):
                        <% onclick = "ExpenseList.payment_form(%s, '%s');" % (expense.id, api.format_amount(expense.topay(), grouping=False)) %>
                        ${table_btn('#popup-payment_form',
                            u"Paiement",
                            u"Saisir un paiement pour cette feuille",
                            icon='plus',
                            onclick=onclick)}
                    % endif
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</div>
</div>
</%block>
<%block name='footerjs'>
ExpenseList.popup_selector = "#${payment_formname}";
% for i in 'year', 'month', 'status', 'owner', 'items':
    $('#${i}-select').change(function(){$(this).closest('form').submit()});
% endfor
</%block>
