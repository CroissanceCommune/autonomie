<%doc>
    * Copyright (C) 2012-2016 Croissance Commune
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
<h3>Éléments requis</h3>
% for indicator in indicators:
<div>
    <span class='btn btn-circle btn-${indicator.status}'>
    <i class="fa icon-${indicator.status}"></i>
    </span>&nbsp;
    % if indicator.file_id:
    ${indicator.file_type.label} :
    <a href="${request.route_path('file', id=indicator.file_object.id, _query={'action': 'download'})}">
        ${indicator.file_object.name} (${api.human_readable_filesize(indicator.file_object.size)})
    </a>
    ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(request, indicator.file_object))}
    % else:
    <b>Un fichier ${indicator.file_type.label} est manquant</b>
    % endif
    <hr />
</div>
% endfor
