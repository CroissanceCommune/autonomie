<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt

  Used to render the user's main menu regarding it's status
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
          <a class="btn btn-navbar" data-target=".menu" data-toggle="collapse">
            >>>
          </a>
          <div class="nav-collapse menu">
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
% endif
% if usermenu is not UNDEFINED:
    <div class="pull-right btn-group">
        <a class="btn dropdown-toggle" href="#" data-toggle="dropdown">
          <i class="icon-user"></i>
          ${request.user.lastname} ${request.user.firstname}
          <span class="caret"></span>
        </a>
            <ul class='dropdown-menu'>
                % for item in usermenu.items:
                ${render_item(item)}
            % endfor
            </ul>
    </div>
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
            <a class="btn btn-navbar" data-target=".submenu" data-toggle="collapse">
              >>>
            </a>
            <div class='nav-collapse submenu'>
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
