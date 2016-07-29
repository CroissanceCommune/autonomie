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
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='actionmenu'>
<div class='row'>
    <div class='col-md-7'>
        ${form|n}
    </div>
    <div class='col-md-4'>
        <table class='table table-bordered'>
            <tr>
                <td class='white_tr'><br /></td>
                <td>Notes de dépense en attente de validation</td>
            </tr>
            <tr>
                <td class='red_tr'><br /></td>
                <td>Notes de dépense validées</td>
            </tr>
            <tr>
                <td class='orange_tr'><br /></td>
                <td>Notes de dépense partiellement payées</td>
            </tr>
            <tr>
                <td class='green_tr'><br /></td>
                <td>Notes de dépense payées</td>
            </tr>
        </table>
    </div>
</div>
</%block>
<%block name="content">
<table class="table table-condensed">
    <thead>
        <tr>
            <th>Identifiant</th>
            <th>Entrepreneur</th>
            <th>Période</th>
            <th>Montant</th>
            <th>Paiements</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % for expense in records:
            <% url = request.route_path('expensesheet', id=expense.id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <%
if expense.status == 'valid':
    css = "red_"
elif expense.status == 'resulted':
    css = "green_"
elif expense.status == 'paid':
    css = "orange_"
else:
    css = "white_"
%>
            <tr class="${css}tr">
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
                    <% url = request.route_path('expensesheet', id=expense.id) %>
                    ${table_btn(url, u'Modifier', u"Voir la note de dépense", icon="pencil" )}
                    <% url = request.route_path('expensexlsx', id=expense.id) %>
                    ${table_btn(url, u'Export', u"Télécharger au format Excel", icon="file" )}
                    % if expense.is_allowed(request, 'paid'):
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
</%block>
<%block name='footerjs'>
ExpenseList.popup_selector = "#${payment_formname}";
% for i in 'year', 'month', 'status', 'owner', 'items':
    $('#${i}-select').chosen({allow_single_deselect: true});
    $('#${i}-select').change(function(){$(this).closest('form').submit()});
% endfor
</%block>
