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
<%block name='afteractionmenu'>
<div class='page-header-block'>
        % if request.has_permission('admin_treasury'):
        <div class='pull-right btn-group'>
            <button type="button" class="btn btn-default dropdown-toggle"
                    data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                <i class='fa fa-file'></i>&nbsp;
                Exporter émargements <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
                <%
                ## We build the link with the current search arguments
                args = request.GET
                url = request.route_path('workshops.xls', _query=args)
                %>
                <li>
                    <a
                        href='${url}'
                        title="Exporter les éléments de la liste">
                        <i class='fa fa-file-excel-o'></i>&nbsp;Excel
                    </a>
                </li>
                <% url = request.route_path('workshops.ods', _query=args) %>
                <li>
                    <a
                        href='${url}'
                        title="Exporter les éléments de la liste">
                        <i class='fa fa-file'></i>&nbsp;ODS
                    </a>
                </li>
                <% url = request.route_path('workshops.csv', _query=args) %>
                <li>
                    <a
                        href='${url}'
                        title="Exporter les éléments de la liste">
                        <i class='fa fa-file'></i>&nbsp;CSV
                    </a>
                </li>
            </ul>
        </div>
        % endif
    % if request.has_permission('add_workshop'):
        <a class='btn btn-primary primary-action'
        href="${request.route_path('workshops', _query=dict(action='new'))}">
            <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Nouvel Atelier
        </a>
    %endif
</div>
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

<div class='panel panel-default page-block'>
<div class='panel-heading'>
${records.item_count} Résultat(s)
</div>
<div class='panel-body'>
    <% is_admin_view = request.context .__name__ != 'company' %>
    <table class="table table-condensed table-hover">
        <thead>
            <tr>
                <th>${sortable("Date", "datetime")}</th>
                <th>Intitulé de l'Atelier</th>
                <th>Animateur(s)/Animatrice(s)</th>
                <th>Nombre de participant(s)</th>
                % if not is_admin_view:
                    <th>Présence</th>
                % else:
                    <th>Horaires</th>
                % endif
                <th class="actions">Actions</th>
            </tr>
        </thead>
        <tbody>
            % for workshop in records:
                % if request.has_permission('edit_workshop', workshop):
                    <% _query=dict(action='edit') %>
                % else:
                    ## Route is company_workshops, the context is the company
                    <% _query=dict(company_id=request.context.id) %>
                % endif
                <% url = request.route_path('workshop', id=workshop.id, _query=_query) %>
                % if request.has_permission('view_workshop', workshop):
                    <% onclick = "document.location='{url}'".format(url=url) %>
                % else :
                    <% onclick = u"alert(\"Vous n'avez pas accès aux données de cet atelier\");" %>
                % endif
                <tr>
                    <td onclick="${onclick}" class="rowlink">
                        ${api.format_date(workshop.datetime)}
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        ${workshop.name}
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        <ul>
                            % for trainer in workshop.trainers:
                                <li>${trainer.label}</li>
                            % endfor
                        </ul>
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        ${len(workshop.participants)}
                    </td>
                    <td>
                        % if is_admin_view:
                            <ul>
                                % for timeslot in workshop.timeslots:
                                    <li>
                                        <% pdf_url = request.route_path("timeslot.pdf", id=timeslot.id) %>
                                        <a href="${pdf_url}"
                                            title="Télécharger la sortie PDF pour impression"
                                            icon='glyphicon glyphicon-file'>
                                            Du ${api.format_datetime(timeslot.start_time)} au \
        ${api.format_datetime(timeslot.end_time)} \
        (${timeslot.duration[0]}h${timeslot.duration[1]})
                                        </a>
                                    </li>
                                % endfor
                            </ul>
                        % else:
                            % for user in request.context.employees:
                                <% is_participant = workshop.is_participant(user.id) %>
                                % if is_participant:
                                    ${api.format_account(user)} :
                                    % for timeslot in workshop.timeslots:
                                        <div>
                                            Du ${api.format_datetime(timeslot.start_time)} \
                                            au ${api.format_datetime(timeslot.end_time)} : \
                                            ${timeslot.user_status(user.id)}
                                        </div>
                                    % endfor
                                % endif
                            % endfor
                        % endif
                    </td>
                    <td class="actions">
                        % if request.has_permission('edit_workshop', workshop):
                            <% edit_url = request.route_path('workshop', id=workshop.id, _query=dict(action="edit")) %>
                            ${table_btn(edit_url, u"Voir/éditer", u"Voir / Éditer l'atelier", icon='pencil')}

                            <% del_url = request.route_path('workshop', id=workshop.id, _query=dict(action="delete")) %>
                            ${table_btn(del_url, \
                            u"Supprimer",  \
                            u"Supprimer cet atelier", \
                            icon='trash', \
                            onclick=u"return confirm('Êtes vous sûr de vouloir supprimer cet atelier ?')", \
                            css_class="btn-danger")}
                        % elif request.has_permission("view_workshop", workshop):
                            ${table_btn(url, u"Voir", u"Voir l'atelier", icon='search')}
                        % endif
                    </td>
                </tr>
            % endfor
            % if len(records) == 0:
            <td colspan="6">Aucun atelier ne correspond à votre recherche</td>
            % endif
        </tbody>
    </table>
    ${pager(records)}
    </div>
</div>
</%block>
