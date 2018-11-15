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
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name="afteractionmenu">
% if request.has_permission('admin.activity'):
<div class='page-header-block'>
<a
    class='btn btn-primary primary-action'
    href="${request.route_path('activities', _query={'action': 'new'})}">
<i class="glyphicon glyphicon-plus-sign"></i>&nbsp;
Programmer un nouveau rendez-vous
</a>
<div class='pull-right btn-group' role='group'>
        <%
    args = request.GET
    url = request.route_path('activities.xls', _query=args)
    %>
    <a
        class='btn btn-default'
        href='${url}'
        title="Exporter les éléments de la liste au format xls">
        <i class='fa fa-file-excel-o'></i>&nbsp;Excel
    </a>
        <%
    args = request.GET
    url = request.route_path('activities.ods', _query=args)
    %>
    <a
        class='btn btn-default'
        href='${url}'
        title="Exporter les éléments de la liste au format ods">
        <i class='fa fa-file'></i>&nbsp;ODS
    </a>
</div>
</div>
% endif
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
<div class='panel-heading'>
<a  href='#filter-form' data-toggle='collapse' aria-expanded="false" aria-controls="filter-form">
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
    <div class='collapse' id='filter-form'>
        <div class='row'>
            <div class='col-xs-12'>
                ${form|n}
            </div>
        </div>
    </div>
</div>
</div>
% if last_closed_event is not UNDEFINED and last_closed_event is not None:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Dernières préconisations
    </div>
    <div class='panel-body'>
        <blockquote>
            ${api.clean_html(last_closed_event.action)|n}
            <footer>le ${api.format_date(last_closed_event.datetime)}</footer>
        </blockquote>
    </div>
</div>
% endif

<div class='panel panel-default page-block'>
<div class='panel-heading'>
${records.item_count} Résultat(s)
</div>
<div class='panel-body'>
    <div class='row'>
        <div class='col-md-4 col-md-offset-8 col-xs-12'>
            <table class='table table-bordered status-table'>
                <tr>
                    <td class='activity-status-planned'><br /></td>
                    <td>Rendez-vous programmés</td>
                </tr>
                <tr>
                    <td class='activity-status-closed'><br /></td>
                    <td>Rendez-vous terminés</td>
                </tr>
                <tr>
                    <td class='activity-status-cancelled'><br /></td>
                    <td>Rendez-vous annulés</td>
                </tr>
            </table>
        </div>
    </div>
    <table class="table table-condensed table-hover status-table">
        <thead>
            <tr>
                <th>${sortable("Horaire", "datetime")}</th>
                <th>${sortable("Conseiller", "conseillers")}</th>
                <th>Participant(s)</th>
                <th>Nature du Rdv</th>
                <th>Mode de Rdv</th>
                <th class="actions">Actions</th>
            </tr>
        </thead>
        <tbody>
            % for activity in records:
                <% url = request.route_path('activity', id=activity.id) %>
                % if request.has_permission('view.activity', activity):
                    <% onclick = "document.location='{url}'".format(url=url) %>
                % else :
                    <% onclick = u"alert(\"Vous n'avez pas accès aux données de ce rendez-vous\");" %>
                % endif
                <tr class="activity-status-${activity.status}">
                    <td onclick="${onclick}" class="rowlink">
                        ${api.format_datetime(activity.datetime)}
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        <ul>
                        % for conseiller in activity.conseillers:
                            <li>${api.format_account(conseiller)}</li>
                        % endfor
                        </ul>
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        <ul>
                        % for participant in activity.participants:
                            <li>${api.format_account(participant)}</li>
                        % endfor
                        </ul>
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        % if activity.type_object is not None:
                            ${activity.type_object.label}
                        % endif
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        ${activity.mode}
                    </td>
                    <td class="actions">
                        % if api.has_permission('edit.activity', activity):
                            <% edit_url = request.route_path('activity', id=activity.id, _query=dict(action="edit")) %>
                            ${table_btn(edit_url, \
                            u"Voir/éditer", \
                            u"Voir / Éditer le rendez-vous", \
                            icon='pencil')}
                            <% pdf_url = request.route_path("activity.pdf", id=activity.id) %>
                            ${table_btn(pdf_url, \
                            u"PDF", \
                            u"Télécharger la sortie PDF pour impression", \
                            icon='file')}
                            <% del_url = request.route_path('activity', id=activity.id, _query=dict(action="delete")) %>
                            ${table_btn(del_url, \
                            u"Supprimer",  \
                            u"Supprimer ce rendez-vous", \
                            icon='trash', \
                            onclick=u"return confirm('Êtes vous sûr de vouloir supprimer ce rendez-vous ?')", \
                            css_class="btn-danger")}
                        % else:
                            ${table_btn(url, \
                            u"Voir", \
                            u"Voir le rendez-vous", \
                            icon='search')}
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
