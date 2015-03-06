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
<%def name='timeslot_row(event)'>
    <% workshop = event.workshop %>
    <% url = request.route_path('workshop', id=workshop.id) %>
    <% onclick = "document.location='{url}'".format(url=url) %>
    <td onclick="${onclick}" class="rowlink visible-lg" >
            Atelier
        </td>
        <td  onclick="${onclick}" class="rowlink" >
            ${api.format_datetime(event.start_time)}
        </td>
        <td onclick="${onclick}" class="rowlink">
            ${', '.join(workshop.leaders)}
        </td>
        <td class="visible-lg rowlink" onclick="${onclick}">
            ${workshop.name} (${event.name})
        </td>
        <td class="visible-lg" style="text-align:right">
            ${table_btn(url, u"Voir", u"Voir l'atelier", icon='search')}
        </td>
</%def>
<%def name='activity_row(event)'>
    <% url = request.route_path('activity', id=event.id) %>
    <% onclick = "document.location='{url}'".format(url=url) %>
    <td onclick="${onclick}" class="rowlink visible-lg" >
            Rendez-vous
        </td>
        <td  onclick="${onclick}" class="rowlink" >
            ${api.format_datetime(event.datetime)}
        </td>
        <td onclick="${onclick}" class="rowlink">
            ${', '.join([api.format_account(conseiller) for conseiller in event.conseillers])}
        </td>
        <td class="visible-lg rowlink" onclick="${onclick}">
            % if event.type_object is not None:
                ${event.type_object.label}
            % endif
             (${event.mode})
        </td>
        <td class="visible-lg" style="text-align:right">
            ${table_btn(url, u"Voir", u"Voir l'évènement", icon='glyphicon glyphicon-search')}
        </td>
</%def>
<div class='section-header'>Vos rendez-vous</div>
Afficher <select id='number_of_events'>
  % for i in (5, 10, 15, 50):
  <option value='${i}'
  % if events.items_per_page == i:
    selected=true
  % endif
  >
  ${i}
  </option>
  % endfor
</select>
éléments à la fois
<table class='table table-stripped'>
    <thead>
        <th class="visible-lg">
            Type
        </th>
        <th>
            Date de début
        </th>
        <th>
            Conseiller / Animateur
        </th>
        <th class="visible-lg">
            Intitulé
        </th>
        <th class="visible-lg">
        </th>
    </thead>
    <tbody>
        % for event in events:
            <tr>
                % if event.type_ == 'activity':
                    ${activity_row(event)}
                % elif event.type_ == 'timeslot':
                    ${timeslot_row(event)}
                % else:
                    ${event.type_}
                % endif
            </tr>
        % endfor
    </tbody>
</table>
${pager(events)}
