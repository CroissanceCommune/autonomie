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
<%inherit file="/layouts/default.mako" />
<%block name='afteractionmenu'>
<div class='page-header-block'>

% if breadcrumb is not UNDEFINED and 'popup' not in request.GET:
    <ul class="breadcrumb breadcrumb-arrow hidden-xs">
        % if back_link:
        <li><a href='${back_link}'><i class='fa fa-chevron-left'></i></a></li>
        % endif
    % for title, url in list(breadcrumb):
        <li
        % if loop.last:
        class='active'
        % endif
        >
        % if not loop.last:
        <a href="${url}">${title}</a>
        % else:
        <span>${title}</span>
        % endif
        </li>
    % endfor
    </ul>
% endif

% if info_message != UNDEFINED:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Message
    </div>
    <div class='panel-body'>
        <div class="alert alert-success">
            ${info_message|n}
        </div>
    </div
</div>
% endif
% if warn_message != UNDEFINED:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Message
    </div>
    <div class='panel-body'>
        <div class="alert alert-warning">
            <i class='fa fa-warning'></i>
            ${warn_message|n}
        </div>
    </div>
</div>
% endif
% if help_message != UNDEFINED:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Message
    </div>
    <div class='panel-body'>
        <div class='alert alert-info'>
        <i class='fa fa-question-circle fa-2x'></i>
        ${help_message|n}
        </div>
    </div>
</div>
% endif
${request.layout_manager.render_panel('admin_nav', context=navigation)}
<%block name='afteradminmenu'>
</%block>
</div>
</%block>
