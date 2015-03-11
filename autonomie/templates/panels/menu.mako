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

<%def name="render_item(elem)">
    <li
    % if elem.get('href') == request.current_route_path():
        class="active"
    % endif
    >
        <a title='${elem.get("title")}' href="${elem.get('href')}">
            % if elem.get('icon'):
                <i class='${elem['icon']}'></i>
            % endif
             ${elem.get('label', "")}
        </a>
    </li>
</%def>
<%def name="render_static(elem)">
    ${elem['html']|n}
</%def>
<%def name="render_dropdown(elem)">
    <li class='dropdown'>
    <a class='dropdown-toggle' data-toggle='dropdown' href='#' role='button' aria-expanded="false">
            ${elem.get('label', '')}
            <span class="caret"></span>
        </a>
        <ul class='dropdown-menu' role="menu">
        % for item in elem.items:
            ${render_item(item)}
        % endfor
        </ul>
    </li>
</%def>
% if menu is not UNDEFINED or usermenu is not UNDEFINED:
    <header class="navbar navbar-inverse hidden-print headmenu">

    <div class="container-fluid">

        <div class="navbar-header">
            <button
                type="button"
                class="navbar-toggle collapsed"
                data-target=".menu"
                data-toggle="collapse"
            >
              <span class="sr-only">Afficher le menu</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href='/'><i class='glyphicon glyphicon-white icon-home'></i>Autonomie</a>
        </div>

        <nav class="navbar-collapse menu collapse ">

    % if  menu is not UNDEFINED:
               <ul
                    % if hasattr(elem, "css"):
                        class="nav navbar-nav ${menu_css}"
                    % else:
                      class="nav navbar-nav"
                    % endif
                    >
                    % for item in menu.items:
                        % if item.__type__ == 'item':
                            ${render_item(item)}
                        % elif item.__type__ == 'static':
                            ${render_static(item)}
                        % elif item.__type__ == 'dropdown':
                            ${render_dropdown(item)}
                        % endif
                    % endfor
              </ul>
    % endif
    % if usermenu is not UNDEFINED:
        <ul class="nav navbar-nav navbar-right">
            <li class="dropdown pull-right">
                <a class="dropdown-toggle" href="#" data-toggle="dropdown">
                    <i class="glyphicon glyphicon-white icon-user"></i>
                  ${request.user.lastname} ${request.user.firstname}
                  <span class="caret"></span>
                </a>
                    <ul class='dropdown-menu'>
                        % for item in usermenu.items:
                        ${render_item(item)}
                        <li class="divider"></li>
                    % endfor
                </ul>
            </li>
         </ul>
    % endif
## We close the main menu
</nav>
    </div>
</header>
% endif
% if submenu is not UNDEFINED:
    ## No usermenu, it's the submenu's bar
    <header class="navbar navbar-inverse hidden-print headmenu">
        <div class="container-fluid">
            <div class="navbar-header">
                <button
                    type="button"
                    class="navbar-toggle collapsed"
                    data-target=".submenu"
                    data-toggle="collapse"
                    >
                      <span class="sr-only">Afficher le sous-menu</span>
                      <span class="icon-bar"></span>
                      <span class="icon-bar"></span>
                      <span class="icon-bar"></span>
                  </button>
              </div>
              <nav class='navbar-collapse submenu collapse'>
                    <ul
                        % if hasattr(elem, "css"):
                            class="nav navbar-nav ${submenu.css}"
                        % else:
                            class='nav navbar-nav'
                        % endif
                        >
                        % for item in submenu.items:
                            % if item.__type__ == 'item':
                                ${render_item(item)}
                            % elif item.__type__ == 'static':
                                ${render_static(item)}
                            % elif item.__type__ == 'dropdown':
                                ${render_dropdown(item)}
                            % endif
                        % endfor
                    </ul>
                </nav>
        </div>
    </header>
% endif
