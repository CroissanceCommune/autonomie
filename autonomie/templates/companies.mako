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
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%block name='actionmenu'>
## We place the search form in the actionmenu since there are a few fields
    <% request.actionmenu.add(form) %>
    ${request.actionmenu.render(request)|n}
</%block>
<%block name="content">
<table class="table table-condensed table-hover">
    <thead>
        <th>${sortable("Nom", "name")}</th>
        <th>Adresse e-mail</th>
        <th>Entrepreneur(s)</th>
        <th class="actions">Actions</th>
    </thead>
    <tbody>
        % for company in records:
            <% url = request.route_path('company', id=company.id, _query=dict(action='edit')) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <tr>
                <td onclick="${onclick}" class="rowlink">
                    ${company.name}
                    % if company.archived:
                    <span class='label label-warning'>Cette entreprise a été archivée</span>
                    % endif
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${company.email}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    <ul>
                        % for user in company.employees:
                            <li>${api.format_account(user)}</li>
                        % endfor
                    </ul>
                </td>
                <td class="actions">
		                <div class='btn-group'>
		                    <button
                                type="button"
                                class="btn btn-default dropdown-toggle"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">
                                Actions <span class="caret"></span>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-right">
                                % for url, label, title, icon, options in stream_actions(company):
                                    ${dropdown_item(url, label, title, icon=icon, **options)}
                                % endfor
                            </ul>
                        </div>
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
