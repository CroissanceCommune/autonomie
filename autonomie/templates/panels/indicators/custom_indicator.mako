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
<div>
    <span class='btn btn-circle btn-${indicator.status}'>
    <i class="fa icon-${indicator.status}"></i>
    </span>&nbsp;
    ${indicator.label}
    % if indicator.forced:
        <em>Cet indicateur a été forcé manuellement</em>
    % endif
    % if request.has_permission('force.indicator', indicator):
    &nbsp;
    &nbsp;
    &nbsp;
    <a
        href="${force_url}"
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
