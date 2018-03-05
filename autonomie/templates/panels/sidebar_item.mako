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
<%def name="render_item(elem)">
    % if elem.has_permission(_context, request):
        <li
        % if elem.selected(_context, request):
            class="active"
        % elif not elem.enabled(_context, request):
            class='disabled'
        % endif
        >
            <a
                title='${elem.title}'
                href="${elem.url(_context, request)}">
                <i class="${elem.icon}"></i>&nbsp;<span class='hidden-xs'>${elem.label|n}</span>
            </a>
        </li>
    % endif
</%def>
<%def name="render_dropdown(elem)">
    % if elem.has_permission(_context, request):
        % if not elem.enabled(_context, request):
        ${render_item(elem)}
        % else:
            <li
                class='dropdown
                % if elem.selected(_context, request):
                    active
                % elif not elem.enabled(_context, request):
                    disabled
                % endif
                '
                >
                <a class='dropdown-toggle' data-toggle='collapse' href='#${elem.name}' role='button' aria-expanded="false">
                    <i class="${elem.icon}"></i>&nbsp;<span class='hidden-xs'>${elem.label|n}</span>
                    <span class="caret"></span>
                </a>
                <ul
                    id="${elem.name}"
                    class='
                    nav subnav
                    collapse
                    % if elem.selected(_context, request):
                    in
                    % endif
                    '
                    role="menu"
                    >
                % for item in elem.items:
                    ${render_item(item)}
                % endfor
                </ul>
            </li>
        % endif
    % endif
</%def>
% if menu.__type__ == 'dropdown':
${render_dropdown(menu)}
% else:
${render_item(menu)}
% endif
