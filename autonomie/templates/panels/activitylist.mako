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
<div class='section-header'>Rendez-vous</div>
Afficher <select id='number_of_activities'>
  % for i in (5, 10, 15, 50):
  <option value='${i}'
  % if activities.items_per_page == i:
    selected=true
  % endif
  >
  ${i}
  </option>
  % endfor
</select>
éléments à la fois
<table class='table table-stripped activitylist'>
    <thead>
        <th>
            Date
        </th>
        <th>
            Conseiller
        </th>
        <th class="visible-desktop">
            Nature du rendez-vous
        </th>
        <th class="visible-desktop">
            Mode de rendez-vous
        </th>
        <th class="visible-desktop">
        </th>
    </thead>
    <tbody>
        % for activity in activities:
            <tr>
                <% url = request.route_path("activity", id=activity.id) %>
                <% onclick = "document.location='{url}'".format(url=url) %>
                <td  onclick="${onclick}" class="rowlink" >
                    ${api.format_date(activity.date)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(activity.conseiller)}
                </td>
                <td class="visible-desktop rowlink" onclick="${onclick}">
                    % if activity.type_object is not None:
                        ${activity.type_object.label}
                    % endif
                </td>
                <td class="visible-desktop rowlink">${activity.mode}</td>
                <td class="visible-desktop" style="text-align:right">
                    ${table_btn(url, u"Voir", u"Voir le rendez-vous", icon='icon-search')}
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(activities)}
