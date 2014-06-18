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
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    % if api.has_permission('manage'):
        <a href="${request.route_path('workshops', _query=dict(action='new'))}">
            Nouvel Atelier
        </a>
    %endif
    </li>
    <li>
    ${form|n}
    </li>
</ul>
</%block>
<%block name="content">
<table class="table table-condensed table-hover">
    <thead>
        <tr>
            <th>${sortable("Date", "date")}</th>
            <th>Intitulé de l'Atelier</th>
            <th>Animateur(s)/Animatrice(s)</th>
            <th>Nombre de participant(s)</th>
            <th>Horaires</th>
            <th style="text-align:center">Actions</th>
        </tr>
    </thead>
    <tbody>
        % for workshop in records:
            <% url = request.route_path('workshop', id=workshop.id) %>
            % if api.has_permission('view', workshop):
                <% onclick = "document.location='{url}'".format(url=url) %>
            % else :
                <% onclick = u"alert(\"Vous n'avez pas accès aux données de cet atelier\");" %>
            % endif
            <tr>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_date(workshop.date)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${workshop.name}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    <ul>
                        % for lead in workshop.leaders:
                            <li>${lead}</li>
                        % endfor
                    </ul>
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${len(workshop.participants)}
                </td>
                <td>
                    <ul>
                        % for timeslot in workshop.timeslots:
                            <li>
                                <% pdf_url = request.route_path("timeslot.pdf", id=timeslot.id) %>
                                <a href="${pdf_url}" title="Télécharger la sortie PDF pour impression" icon='icon-file'>
                                    Du ${api.format_date(timeslot.start_time)} au ${api.format_date(timeslot.end_time)}
                                </a>
                            </li>
                        % endfor
                    </ul>
                </td>
                <td>
                    % if api.has_permission("view", workshop):
                        ${table_btn(url, u"Voir", u"Voir l'atelier", icon='icon-search')}
                    % endif
                    % if api.has_permission('edit', workshop):
                        <% edit_url = request.route_path('workshop', id=workshop.id, _query=dict(action="edit")) %>
                        ${table_btn(edit_url, u"Voir/éditer", u"Voir / Éditer l'atelier", icon='icon-pencil')}

                        <% del_url = request.route_path('workshop', id=workshop.id, _query=dict(action="delete")) %>
                        ${table_btn(del_url, u"Supprimer",  u"Supprimer cet atelier", icon='icon-trash', onclick=u"return confirm('Êtes vous sûr de vouloir supprimer cet atelier ?')")}

                    % endif
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
