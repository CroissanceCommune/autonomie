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
<div id='js-main-area' class='task-edit'></div>
</%block>
<%block name='footer'>
<script type='text/javascript'>
var AppOption = {};
AppOption['context_url'] = "${request.route_path('/api/v1/' + request.context.type_ + 's/{id}', id=request.context.id)}";
AppOption['load_url'] = "${request.route_path('/api/v1/' + request.context.type_ + 's/{id}', id=request.context.id, _query={'form_options': '1'})}";
</script>
<script type='text/javascript' src="${request.static_url('autonomie:static/js/build/task.js')}" ></script>
</%block>
