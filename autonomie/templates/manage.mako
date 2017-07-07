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
<%inherit file="${context['main_template'].uri}" />
<%block name="content">
<br />
<div class='row'>
    <div class='col-md-6'>
        % for dataset, table_title, perm in (\
            (estimations, u"Devis en attente", "valid.estimation"), \
            (invoices, u"Factures et Avoirs en attente", "valid.invoice"), \
        ):
        % if request.has_permission(perm):
    <div class="panel panel-info">
        <div class="panel-heading">
            ${table_title}
        </div>
        <table class="table table-striped table-condensed table-hover">
            <thead>
                <tr>
                    <th>Type de document</th>
                    <th>Entreprise</th>
                    <th>Demandé le</th>
                </tr>
            </thead>
            <tbody>
            % for task in dataset:
                <tr class="clickable-row" data-href="${task.url}">
                    <td>
                        ${api.format_task_type(task)}
                    </td>
                    <td>
                        ${task.get_company().name}
                    </td>
                    <td>
                        ${api.format_date(task.status_date)}
                    </td>
                </tr>
            % endfor
        % if not dataset:
            <tr><td colspan='3'>Aucun document en attente</td></tr>
        % endif
            </tbody>
        </table>
    </div>
    % endif
% endfor
<div class="panel panel-info">
    <div class="panel-heading">Mes Activités / Rendez-vous à venir</div>
    <table class="table table-striped table-condensed table-hover">
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
                <tr class="clickable-row" data-href="${activity.url}">
                    <td>
                        ${api.format_datetime(activity.datetime)}
                    </td>
                    <td>
                        <ul>
                        % for participant in activity.participants:
                            <li>${api.format_account(participant)}</li>
                        % endfor
                        </ul>
                    </td>
                    <td>
                        ${activity.mode}
                    </td>
                    <td>
                        ${activity.type_object.label}
                    </td>
                </tr>
            % endfor
            % if not activities:
                <tr><td colspan='4'>Aucune activité n'est prévue</td></tr>

            % else:
                <a
                    class='btn btn-primary btn-sm'
                    href="${request.route_path('activities', _query=dict(conseiller_id=request.user.id))}"
                    >
                    Voir plus
                </a>
            % endif
        </tbody>
    </table>
</div>
</div>
% if request.has_permission('admin_expense'):
<div class='col-md-6'>
    <div class="panel panel-info">
        <div class="panel-heading">
            Les feuilles de notes de dépense en attente
        </div>
        <table class="table table-striped table-condensed table-hover">
            <thead>
                <tr>
                    <th>Période</th>
                    <th>Entrepreneur</th>
                    <th>Demandé le</th>
                </tr>
            </thead>
            <tbody>
        % for expense in expenses:
            <tr class="clickable-row" data-href="${expense.url}">
                <td>
                    ${api.month_name(expense.month)} ${expense.year}
                </td>
                <td>
                    ${api.format_account(expense.user)}
                </td>
                <td>
                    ${api.format_date(expense.status_date)}
                </td>
            </tr>
        % endfor
        % if not expenses:
            <tr><td colspan='3'>Aucun document en attente</td></tr>
        % endif
            </tbody>
        </table>
    </div>
</div>
</div>
% endif
</%block>
