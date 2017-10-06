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

<%inherit file="/admin/index.mako"></%inherit>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    ${title}
    </div>
    <div class='panel-body'>
        <div class='row'>
            <div class='col-md-3'>
                <ul class="nav nav nav-pills nav-stacked" role="tablist">
                <% current = request.params.get('__formid__', forms.keys()[0]) %>
                % for form_name, form_datas in forms.items():
                    <li role="presentation" class="
                    % if form_name == current:
                    active
                    % endif
                    ">
                        <a
                            href="#${form_name}-container"
                            aria-controls="${form_name}-container"
                            role="tab"
                            data-toggle="tab"
                            tabindex='-1'
                            >
                            ${form_datas['title']}
                        </a>
                    </li>
                % endfor
                </ul>
            </div>

             <div class='col-md-6 col-md-offset-1'>

                <div class='tab-content'>
                % for form_name, form_datas in forms.items():
                    <div
                        role="tabpanel"
                        class="tab-pane fade
                        % if form_name == current:
                            in active
                        % endif
                        "
                        id="${form_name}-container"
                    >
                    % if form_name == current and check_messages is not None:
                        <div class="alert alert-info">
                            ${check_messages['title']}
                        </div>
                        % if check_messages['errors']:
                        <div class="alert alert-danger">
                        <p class='text-danger'>
                        % for message in check_messages['errors']:
                            <b>*</b> ${message|n}<br />
                        % endfor
                        </p>
                        </div>
                    % endif
                % endif
                        ${form_datas['form']|n}
                    </div>
                % endfor
            </div>
        </div>
    </div>
</div>
</%block>

