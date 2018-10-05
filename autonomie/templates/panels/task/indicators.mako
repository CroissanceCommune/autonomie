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
% for indicator in indicators:
<div>
    <span class='btn btn-circle btn-${indicator.status}'>
    <i class="fa icon-${indicator.status}"></i>
    </span>&nbsp;
    ${indicator.file_type.label} :

    % if indicator.file_id:
        <a href="#" onclick="openPopup('${request.route_path('file', id=indicator.file_object.id)}')">
            ${indicator.file_object.name} (${api.human_readable_filesize(indicator.file_object.size)})
        </a>
        % if request.has_permission('valid.indicator', indicator):
        &nbsp;<em>fichier en attente de validation</em>
        <a
            href="${request.route_path(force_route, id=indicator.id, _query={'action': 'validation_status', 'validation_status': 'valid'})}"
            class='btn btn-success btn-circle'
            title="Valider le fichier fourni"
            >
                <i class='fa fa-eye'></i>
        </a>
        <a
            href="${request.route_path(force_route, id=indicator.id, _query={'action': 'validation_status', 'validation_status': 'valid'})}"
            class='btn btn-danger btn-circle'
            title="Invalider le fichier fourni"
            >
                <i class='fa fa-close'></i>
        </a>
        % endif
    % elif indicator.forced:
        Cet indicateur a été forcé manuellement
    % else:
        <b>Aucun fichier fourni</b>
    % endif
    % if request.has_permission('add.file', indicator):
    <button
        class='btn btn-default btn-circle'
        onclick="window.openPopup('${file_add_url}?file_type_id=${indicator.file_type_id}')"
        title="Ajouter un fichier"
        >
            <i class='fa fa-plus'></i>
    </button>
    % endif
    % if request.has_permission('force.indicator', indicator):
    &nbsp;
    &nbsp;
    &nbsp;
    <a
        href="${request.route_path(force_route, id=indicator.id, _query={'action': 'force'})}"
        class='btn btn-warning btn-circle'
        % if not indicator.forced:
        onclick="return confirm('Êtes-vous sûr de vouloir forcer cet indicateur (il apparaîtra désormais comme valide) ?');"
        title="Forcer cet indicateur"
        % else:
        title="Invalider cet indicateur"
        % endif
        >
            % if not indicator.forced:
            <i class='fa fa-flash'></i>
            % else:
            <i class='fa fa-undo'></i>
            % endif

    </a>
    % endif
    <hr />
</div>
% endfor
