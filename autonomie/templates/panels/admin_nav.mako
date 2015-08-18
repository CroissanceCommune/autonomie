<%doc>
    * Copyright (C) 2012-2015 Croissance Commune
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
Admin menu panel
</%doc>
<%def name="render_item(elem)">
    <li>
    <a title='${elem.get("title")}' href="${request.route_path(elem.get('path'))}">
        % if elem.get('icon'):
        <i class='${elem['icon']}'></i>
        % endif
        ${elem.get('label', "")} <span class='help-block'>${elem.get('title', '')}</span>
    </a>
    </li>
</%def>
% if menus is not UNDEFINED and len(menus) > 0:
    <ul class='nav nav-pills nav-stacked'>
        % for menu_entry in menus:
            ${render_item(menu_entry)}
        % endfor
    </ul>
% endif
