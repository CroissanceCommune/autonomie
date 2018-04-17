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
<%block name="mainblock">
% for template in templates:
<% url = request.current_route_path(_query=dict(template_id=template.id)) %>
    <li>
        <a href="${url}">
            <i class="fa fa-file fa-1x"></i>
            ${template.description} ( ${template.name} )
        </a>
    </li>
% endfor
</ul>
<div class='alert alert-info'>
% if templates == []:
    <i class='fa fa-question-circle fa-2x'></i>
    Vous devez déposer des modèles de document dans Autonomie pour pouvoir accéder à cet outil.
        <br />
% endif
% if request.has_permission('admin'):
    <a class='btn btn-success'
        href="${admin_url}">
    <i class="glyphicon glyphicon-plus"></i>
        Déposer de nouveau modèle de document
    </a>
% endif
</div>
</%block>
