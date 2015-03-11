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
<%block name='actionmenu'>
## We place the search form in the actionmenu since there are a few fields
    <% request.actionmenu.add(form) %>
    ${request.actionmenu.render(request)|n}
</%block>
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
                % if not request.user.is_contractor() and user.userdatas is not None:
                    <% url = request.route_path('userdata', id=user.userdatas.id) %>
                % else:
                    <% url = request.route_path('user', id=user.id) %>
                %endif
                <tr class="clickable-row" data-href="${url}">
                    <td><a href="${url}">${api.format_account(user)}</a></td>
                    <td>${user.email}</td>
                    <td>
                        <ul class="list-unstyled">
                            % for company in user.companies:
                                <% company_url = request.route_path('company', id=company.id) %>
                                <li>
                                <a href="${company_url}">${company.name} (<small>${company.goal}</small>)</a>
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
