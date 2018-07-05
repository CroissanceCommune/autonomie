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
    <div class='panel-heading '>
        <div class='row'>
            <div class='col-md-3 col-xs-12 bordered'>
                <div class='row'>
                    <div class='col-md-3 text-center'>
                    % if layout.current_business_object.closed:
                        <i class='fa fa-folder fa-4x'></i>
                    % else:
                        <i class='fa fa-folder-open fa-4x'></i>
                    % endif
                    </div>
                    <div class='col-md-9'>
                        <div>${layout.current_business_object.business_type.label}  : ${layout.current_business_object.name}</div>
                        % if layout.current_business_object.closed:
                        <div class='help-text'>
                        Cette affaire est clôturée
                        </div>
                        % endif
                        <div class'btn-group'>
                        % if request.has_permission("edit.business", layout.current_business_object):
                        <a
                            class='btn btn-default btn-small'
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
            <%block name='businesstitle'>
            </%block>
                % if request.has_permission('close.business', layout.current_business_object):
                <a
                    class='btn btn-default'
                    href="${layout.close_url}"
                    >
                    <i class='fa fa-window-close'></i>&nbsp;Clôturer cette affaire
                </a>
                % endif
            </div>
        </div>
    </div>
    <div class='panel-body'>
        <div class='row'>
            <div class='col-md-3'>
            <%block name='rightblock'>
                ${request.layout_manager.render_panel('sidebar', layout.businessmenu)}
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
