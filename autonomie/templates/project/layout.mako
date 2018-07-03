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
<%block name="headtitle">
<div id='popupmessage'>
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
        <div class='row'>
            <div class='col-md-3 col-xs-12 bordered'>
                <div class='row'>
                    <div class='col-md-3 text-center'>
                        <i class='fa fa-folder-open fa-4x'></i>
                    </div>
                    <div class='col-md-9'>
                        <div>Projet : ${layout.current_project_object.name}</div>
                        <div class='help-text'>
                        % if layout.current_project_object.description:
                            ${layout.current_project_object.description}
                        % endif
                            % if layout.current_project_object.project_type.name != 'default':
                            <br />
                            ${layout.current_project_object.project_type.label}
                            % endif
                        </div>
                        <div>
                        % if request.has_permission("edit.project", layout.current_project_object):
                        <a
                            class='btn btn-default btn-small pull-right'
                            href="${layout.edit_url}"
                            >
                            <i class='fa fa-pencil'></i>
                        </a>
                        % endif
                        </div>
                    </div>
                </div>
            </div>
            <div class='col-md-9 hidden-xs'>
            <%block name='projecttitle'>
                <div>Clients : ${','.join(layout.customer_names)}</div>
            </%block>
            </div>
        </div>
    </div>
    <div class='panel-body'>
        <div class='row'>
            <div class='col-md-3'>
            <%block name='rightblock'>
                ${request.layout_manager.render_panel('sidebar', layout.projectmenu)}
            </%block>
            </div>
            <div class='col-md-9'>
            <%block name='mainblock'>
                Main
            </%block>
            </div>
        </div>
    </div>
</div>
</%block>
