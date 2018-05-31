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
<%inherit file="${context['main_template'].uri}" />
<%block name='mainblock'>
<div class='row'>
    <div class='col-xs-12'>
        <div class='panel panel-default page-block'>
            <div class='panel-heading'>
                <div class='row'>
                <div class='col-md-3 col-xs-12 bordered'>
                    <h4>${request.context.name}</h4>
                    <small>${request.context.business_type.label}</small>
                    % if request.has_permission("edit.business", request.context):
                    <a
                        class='btn btn-default btn-small pull-right'
                        href="${edit_url}"
                        >
                        <i class='fa fa-pencil'></i>
                    </a>
                    % endif
                </div>
                </div>
            </div>
            <div class='panel-body'>
            </div>
        </div>
    </div>
</div>
</%block>
