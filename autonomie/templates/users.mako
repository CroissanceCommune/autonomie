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
    Directory templates, list users and companies
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>${sortable("Nom", "name")}</th>
            <th>${sortable("E-mail", "email")}</th>
            <th>Entreprises</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for user in records:
                <tr>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >${api.format_account(user, reverse=True)}</td>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >${user.email}</td>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >
                        <ul>
                            % for company in user.companies:
                                <li>
                                    ${company.name}
                                    % if not company.enabled():
                                        <span class='label label-warning'>Cette entreprise a été désactivée</span>
                                    % endif
                                </li>
                            % endfor
                        </ul>
                    </td>
                </tr>
            % endfor
        % else:
            <tr><td colspan='3'>Aucun utilisateur n'est présent dans la base</td></tr>
        % endif
</tbody></table>
${pager(records)}
</%block>
