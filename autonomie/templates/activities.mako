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
        <a href="${request.route_path('activities', _query=dict(action='new'))}">
            Nouveau rendez-vous
        </a>
    %endif
    </li>
</ul>
<div class='row-fluid'>
<div class='span8'>
    <div class='row'>
        ${form|n}
    </div>
</div>
        <div class='span4'>
        <table class='table table-bordered'>
            <tr>
                <td class='white_tr'><br /></td>
                <td>Rendez-vous programmés</td>
            </tr>
            <tr>
                <td class='green_tr'><br /></td>
                <td>Rendez-vous terminés</td>
            </tr>
            <tr>
                <td class='orange_tr'><br /></td>
                <td>Rendez-vous annulés</td>
            </tr>
        </table>
    </div>
</div>

</%block>
<%block name="content">
<table class="table table-condensed table-hover">
    <thead>
        <tr>
            <th>${sortable("Date", "date")}</th>
            <th>${sortable("Conseiller", "conseiller")}</th>
            <th>Participant(s)</th>
            <th>Nature du Rdv</th>
            <th>Mode de Rdv</th>
            <th style="text-align:center">Actions</th>
        </tr>
    </thead>
    <tbody>
        % for activity in records:
            <% url = request.route_path('activity', id=activity.id) %>
            % if api.has_permission('view', activity):
                <% onclick = "document.location='{url}'".format(url=url) %>
            % else :
                <% onclick = u"alert(\"Vous n'avez pas accès aux données de ce rendez-vous\");" %>
            % endif
            <%
if activity.status == 'planned':
    css = "white_"
elif activity.status == 'cancelled':
    css = "orange_"
elif activity.status == 'closed':
    css = "green_"
%>
            <tr class='${css}tr'>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_date(activity.date)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(activity.conseiller)}
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
                <td>
                    % if api.has_permission("view", activity):
                        ${table_btn(url, u"Voir", u"Voir le rendez-vous", icon='icon-search')}
                    % endif
                    % if api.has_permission('edit', activity):
                        <% edit_url = request.route_path('activity', id=activity.id, _query=dict(action="edit")) %>
                        ${table_btn(edit_url, u"Voir/éditer", u"Voir / Éditer le rendez-vous", icon='icon-pencil')}
                        <% del_url = request.route_path('activity', id=activity.id, _query=dict(action="delete")) %>
                        ${table_btn(del_url, u"Supprimer",  u"Supprimer ce rendez-vous", icon='icon-trash', onclick=u"return confirm('Êtes vous sûr de vouloir supprimer ce rendez-vous ?')")}
                        <% pdf_url = request.route_path("activity.pdf", id=activity.id) %>
                        ${table_btn(pdf_url, u"PDF", u"Télécharger la sortie PDF pour impression", icon='icon-file')}
                    % endif
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
