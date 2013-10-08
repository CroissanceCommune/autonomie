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

<%doc>
    Template for the page showing the document waiting for approval
</%doc>
<%inherit file="/base.mako"></%inherit >
<%block name="content">
<br />
<table class="table table-striped table-condensed table-hover table-bordered">
    <caption>Devis, Factures et Avoirs</caption>
    <thead>
        <tr>
            <th>Entreprise</th>
            <th>Nom du document</th>
            <th>Statut</th>
        </tr>
    </thead>
    <tbody>
% for task in tasks:
    <tr>
        <td onclick="document.location='${task.url}'" class='rowlink'>
            ${task.get_company().name}
        </td>
        <td onclick="document.location='${task.url}'" class='rowlink'>
            ${task.name}
        </td>
        <td onclick="document.location='${task.url}'" class='rowlink'>
            ${api.format_status(task)}
        </td>
    </tr>
% endfor
% if not tasks:
    <tr><td colspan='3'>Aucun document en attente</td></tr>
% endif
    </tbody>
</table>
<br />
<table class="table table-striped table-condensed table-hover table-bordered">
<caption>Feuilles de notes de frais</caption>
    <thead>
        <tr>
            <th>Période</th>
            <th>Statut</th>
        </tr>
    </thead>
    <tbody>
% for expense in expenses:
    <tr>
        <td onclick="document.location='${expense.url}'" class='rowlink'>
            ${api.month_name(expense.month)} ${expense.year}
        </td>
        <td onclick="document.location='${expense.url}'" class='rowlink'>
            ${api.format_expense_status(expense)}
        </td>
    </tr>
% endfor
% if not expenses:
    <tr><td colspan='3'>Aucun document en attente</td></tr>
% endif
    </tbody>
</table>
</%block>
