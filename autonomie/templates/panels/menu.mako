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
        <a class='dropdown-toggle' data-toggle='dropdown' href='#'>
            ${elem.get('label', '')}
        <b class="caret"></b>
        </a>
        <ul class='dropdown-menu'>
        % for item in elem.items:
            ${render_item(item)}
        % endfor
        </ul>
    </li>
</%def>
% if  menu is not UNDEFINED:
    <div class="navbar navbar-inverse">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href='/'><i class='icon-white icon-home'></i>Autonomie</a>
          <button class="btn btn-navbar" data-target=".menu" data-toggle="collapse" type="button">
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
          </button>
          <div class="nav-collapse menu collapse">
            <ul
                % if hasattr(elem, "css"):
                    class="nav ${menu.css}"
                % else:
                    class='nav'
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
                    <li class='divider-vertical'></li>
                % endfor
            </ul>
% elif usermenu is not UNDEFINED:
    ## Is there is no menu, but there is a usermenu, we need to display it
    <div class="navbar navbar-inverse">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href='/'><i class='icon-white icon-home'></i>Autonomie</a>
          <button class="btn btn-navbar" data-target=".menu" data-toggle="collapse" type="button">
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
          </button>
          <div class="nav-collapse menu collapse">
% endif
% if usermenu is not UNDEFINED:
    <ul class="nav pull-right">
        <li class="dropdown pull-right">
            <a class="dropdown-toggle" href="#" data-toggle="dropdown">
                <i class="icon-white icon-user"></i>
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
</div>
</div>
</div>
</div>
% endif
% if submenu is not UNDEFINED:
    ## No usermenu, it's the submenu's bar
        <div class="navbar navbar-inverse">
        <div class="navbar-inner">
          <div class="container">
              <button class="btn btn-navbar" data-target=".submenu" data-toggle="collapse" type="button">
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
              </button>
              <div class='nav-collapse submenu collapse'>
    <ul
        % if hasattr(elem, "css"):
            class="nav ${submenu.css}"
        % else:
            class='nav'
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
            <li class='divider-vertical'></li>
        % endfor
    </ul>
</div>
</div>
</div>
</div>
% endif
