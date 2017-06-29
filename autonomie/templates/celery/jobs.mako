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
<div class='row'>
<div class='col-md-8'>
    <div class='row'>
        ${form|n}
    </div>
</div>
        <div class='col-md-4'>
        <table class='table table-bordered status-table'
            <tr>
                <td class='job-planned'><br /></td>
                <td>Tâches planifiées</td>
            </tr>
            <tr>
                <td class='job-completed'><br /></td>
                <td>Tâches terminées</td>
            </tr>
            <tr>
                <td class='job-failed'><br /></td>
                <td>Tâches échouées</td>
            </tr>
        </table>
    </div>
</div>

</%block>
<%block name="content">
<table class="table table-condensed table-hover status-table">
    <thead>
        <tr>
            <th>${sortable(u"Date d'éxécution", "created_at")}</th>
            <th>Type de tâche</th>
            <th>Statut</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % for job in records:
            <% url = request.route_path('job', id=job.id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <%
elif job.status == 'completed':
    css = "green_"
%>
            <tr class='job-${job.status}'>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_datetime(job.created_at)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${job.label}
                </td>
                <td onclick="${onclick}" class="rowlink">
                </td>
                <td class="actions">
                    <% view_url = request.route_path('job', id=job.id) %>
                    ${table_btn(view_url, u"Voir", u"Voir la tâche", icon='pencil')}
                    <% del_url = request.route_path('job', id=job.id, _query=dict(action="delete")) %>
                    ${table_btn(\
                    del_url, \
                    u"Supprimer",  \
                    u"Supprimer cette entrée d'historique", \
                    icon='trash', \
                    onclick=u"return confirm('Êtes vous sûr de vouloir supprimer cette entrée d'historique ?')", css_class="btn-danger")}
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
