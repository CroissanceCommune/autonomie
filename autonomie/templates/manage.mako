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
<div class='row-fluid'>
    <div class='span6'>
<table class="table table-striped table-condensed table-hover table-bordered">
    <caption>Les devis, factures et avoirs en attent</caption>
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
    <tr><td colspan='3'>aucun document en attente</td></tr>
% endif
    </tbody>
</table>
<table class="table table-striped table-condensed table-hover table-bordered">
    <caption>Mes Activités / Rendez-vous à venir</caption>
    <thead>
        <tr>
            <th>Date</th>
            <th>Participant</th>
            <th>Mode</th>
            <th>Nature du rendez-vous</th>
        </tr>
    </thead>
    <tbody>
        % for activity in activities:
            <tr>
                <td onclick="document.location='${activity.url}'" class='rowlink'>
                    ${api.format_datetime(activity.datetime)}
                </td>
                <td onclick="document.location='${activity.url}'" class='rowlink'>
                    <ul>
                    % for participant in activity.participants:
                        <li>${api.format_account(participant)}</li>
                    % endfor
                    </ul>
                </td>
                <td onclick="document.location='${activity.url}'" class='rowlink'>
                    ${activity.mode}
                </td>
                <td onclick="document.location='${activity.url}'" class='rowlink'>
                    ${activity.type_object.label}
                </td>
            </tr>
        % endfor
        % if not activities:
            <tr><td colspan='4'>aucune activité n'est prévue</td></tr>
    % endif
    </tbody>
</table>
<a
    class='btn btn-primary'
    href="${request.route_path('activities', _query=dict(conseiller_id=request.user.id))}"
    >
    Voir plus
</a>
</div>
<div class='span6'>
<table class="table table-striped table-condensed table-hover table-bordered">
    <caption>Les feuilles de notes de frais en attente</caption>
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
</div>
</%block>
