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

<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="urlbuild" />
<%block name='content'>
<table class="table table-striped table-condensed table-hover">
    <thead>
        <tr>
            <th>${sortable(u"Code", "code")}</th>
            <th>${sortable(u"Nom", "name")}</th>
            <th>Clients</th>
            <th style="text-align:center">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for project in records:
                <tr class='tableelement' id="${project.id}">
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.code}</td>
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.name}</td>
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>
                        <ul>
                            % for customer in project.customers:
                                <li>
                                ${customer.name}
                                </li>
                            % endfor
                        </ul>
                    </td>
                    <td style="text-align:right">
                        % for btn in item_actions:
                            ${btn.render(request, project)|n}
                        % endfor
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun projet n'a été créé pour l'instant
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(records)}
</%block>
