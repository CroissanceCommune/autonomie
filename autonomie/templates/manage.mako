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
<%block name='afteractionmenu'>
<div class='page-header-block'>
<h3>Bonjour ${api.format_account(request.user)}</h3>
<div class='row'>
% if activities:
<div class='col-md-4 col-xs-12'>
<small>Vous avez ${len(activities)} rendez-vous programmés</small>
<ul class='list-group'>
% for activity in activities[:5]:
<li class='list-group-item clickable-row' data-href="${activity.url}">
    <span class='pull-right'>${api.format_datetime(activity.datetime)}</span>
    <span class='label label-info'>${loop.index + 1}</span>&nbsp;
    ${', '.join(api.format_account(p) for p in activity.participants)}
    <br />
</li>
% endfor
</div>
</div>
% endif
</div>
</div>
</%block>
<%block name="content">
<div class='row'>
    <div class='col-md-6'>
        % for dataset, table_title, perm in (\
            (estimations, u"Devis en attente de validation", "valid.estimation"), \
            (invoices, u"Factures et Avoirs en attente de validation", "valid.invoice"), \
        ):
        % if request.has_permission(perm):
    <div class="panel panel-default page-block">
        <div class="panel-heading">
            ${table_title}
        </div>
        <div class='panel-body'>
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
    </div>
    % endif
% endfor
<div class="panel panel-default page-block">
    <div class="panel-heading">Mes Activités / Rendez-vous à venir</div>
        <div class='panel-body'>
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
                    href="${request.route_path('activities', _query=dict(__formid__='deform', conseiller_id=request.user.id))}"
                    >
                    Voir plus
                </a>
            % endif
        </tbody>
    </table>
    </div>
</div>
</div>
% if request.has_permission('admin_expense'):
<div class='col-md-6'>
    <div class="panel panel-default  page-block">
        <div class="panel-heading">
            Les feuilles de notes de dépense en attente de validation
        </div>
        <div class='panel-body'>
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
</div>
% endif
</%block>
