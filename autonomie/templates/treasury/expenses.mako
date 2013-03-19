<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
  Template that display the list of expenses
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
% for user in users:
    <table class="table table-condensed table-borderer">
        <caption><b>Feuille de notes de frais de ${api.format_account(user)}</b></caption>
    <thead>
        <th>Période</th>
        <th>Statut</th>
        <th>Actions</th>
    </thead>
    <tbody>
        % for expense in user.expenses:
            <tr><td>${api.month_name(expense.month)} ${expense.year}</td>
                <td>${api.format_expense_status(expense)}</td>
                <td>
                    <a class='btn' href="${request.route_path('expense', id=expense.id)}">Voir</a>
                </td>
            </tr>
        % endfor
        % if not user.expenses:
            <tr><td colspan='3'>Il n'y a aucun document</td></tr>
        % endif
    </tbody>
</table>
% endfor
</%block>
