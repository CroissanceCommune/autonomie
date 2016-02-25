<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
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
<%doc>
 Task list panel template
</%doc>
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/utils.mako" import="format_customer" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<div class='section-header'>Dernières activités sur vos documents</div>
Afficher <select id='number_of_tasks'>
  % for i in (5, 10, 15, 50):
  <option value='${i}'
  % if tasks.items_per_page == i:
    selected=true
  % endif
  >
  ${i}
  </option>
  % endfor
</select>
éléments à la fois
<table class='table table-stripped tasklist'>
    <thead>
        <th class="visible-lg col-xs-4">
            Nom du document
        </th>
        <th class='col-xs-3'>
            Client
        </th>
        <th class="visible-lg col-xs-3">
            Dernière modification
        </th>
        <th class="visible-lg col-xs-2 text-right">
            Actions
        </th>
    </thead>
    <tbody>
        % for task in tasks:
            <tr>
                <% url = request.route_path(task.type_, id=task.id) %>
                <% onclick = "document.location='{url}'".format(url=url) %>
                <td class="visible-lg rowlink" onclick="${onclick}">
                    ${task.name}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${format_customer(task.customer, False)}
                </td>
                <td class="visible-lg rowlink">${api.format_status(task, full=False)}</td>
                <td class="visible-lg" style="text-align:right">
                    <div class='btn-group'>
                    ${table_btn(request.route_path(task.type_, id=task.id), u"", u"Voir ce document", icon=u"search")}
                    ${table_btn(
                        request.route_path(task.type_, id=task.id, _query=dict(view='pdf')),
                        u"",
                        u"Télécharger ce document au format pdf",
                        icon=u"fa fa-file-pdf-o")}
                    </div>
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(tasks)}
