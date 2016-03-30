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

<%namespace file="/base/utils.mako" import="table_btn"/>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
% if conf_msg is not UNDEFINED:
    <br /><br />
    <div class='row'>
        <div class='col-md-6 col-md-offset-3'>
            <div class="alert alert-danger">
                ${conf_msg}
            </div>
        </div>
    </div>
% else:
    % for year, values in expense_sheets.items():
            <div class='section-header'>
                <a href="#" data-toggle='collapse' data-target='#year_${year}'>
                    <div>
                        <i style="vertical-align:middle" class="glyphicon glyphicon-folder-open"></i>&nbsp;${year}
                    </div>
                </a>
            </div>
            % if year == current_year:
                <div class="section-content in collapse" id='year_${year}'>
            %else:
                <div class="section-content collapse" id='year_${year}'>
            %endif
        % for user, expenses in values:
        <table class="table table-condensed table-bordered">
            <caption>
                <b>Feuille de notes de dépense de ${api.format_account(user)}</b>
                ${user_buttons[user.id].render(request)|n}
            </caption>
        <thead>
            <th>Période</th>
            <th>Statut</th>
            <th>Total</th>
            <th>Paiements</th>
            <th>Actions</th>
        </thead>
        <tbody>
            % for expense in expenses:
                <tr><td>${api.month_name(expense.month)} ${expense.year}</td>
                    <td>${api.format_expense_status(expense)}</td>
                    <td>${api.format_amount(expense.total, trim=True)|n}</td>
                    <td>
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
                    <td style='text-align:right'>
                        ${table_btn(request.route_path('expensesheet', id=expense.id), u"Voir", u"Voir cette note de dépense", 'search')}
                        ${table_btn(request.route_path('expensexlsx', id=expense.id), u"Export", u"Exporter cette note de dépense au format xslx", "file")}
                    </td>
                </tr>
            % endfor
            % if not expenses:
                <tr><td colspan='4'>Il n'y a aucun document</td></tr>
            % endif
        </tbody>
    </table>
    % endfor
</div>
    % endfor
% endif
</%block>
