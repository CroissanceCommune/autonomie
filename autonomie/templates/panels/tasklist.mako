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
        <th class="visible-desktop">
            Nom du document
        </th>
        <th>
            Projet
        </th>
        <th>
            Client
        </th>
        <th class="visible-desktop">
            Dernière modification
        </th>
        <th class="visible-desktop">
        </th>
    </thead>
    <tbody>
        % for task in tasks:
            <tr>
                <% url = request.route_path(task.type_, id=task.id) %>
                <% onclick = "document.location='{url}'".format(url=url) %>
                <td class="visible-desktop rowlink" onclick="${onclick}">
                    ${task.name}
                </td>
                <td  onclick="${onclick}" class="rowlink" >
                    ${format_project(task.project, False)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${format_customer(task.customer, False)}
                </td>
                <td class="visible-desktop rowlink">${api.format_status(task)}</td>
                <td class="visible-desktop" style="text-align:right">
                    ${table_btn(request.route_path(task.type_, id=task.id), u"Voir", u"Voir ce document", icon=u"icon-search")}
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(tasks)}
