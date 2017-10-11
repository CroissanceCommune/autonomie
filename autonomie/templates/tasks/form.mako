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
<%block name="content">
% if request.context.status == 'wait':
<div class='container-fluid beforeContent'>
    <div class='row'>
        <div class='col-xs-12 col-md-10 col-md-offset-1'>
            <h4>
            ${api.format_status(request.context)}
            </h4>
        </div>
    </div>
</div>
% endif
<div id='js-main-area' class='task-edit'></div>
</%block>
<%block name='footerjs'>
var AppOption = {};
AppOption['context_url'] = "${context_url}";
AppOption['form_config_url'] = "${form_config_url}"
AppOption['load_catalog_url'] = "${load_catalog_url}";
</%block>
