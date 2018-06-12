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
<%namespace file="/base/utils.mako" import="table_btn"/>
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
<hr/>
<h4>Documents générés depuis Autonomie</h4>
<span class='help-block'>
    <i class='fa fa-question-circle fa-2x'></i>
    Chaque fois qu'un utilisateur génère un document depuis cette page, une entrée est ajoutée à l'historique.<br />
    Si nécessaire, pour rendre plus pertinente cette liste, vous pouvez supprimer certaines entrées.
</span>
<table class='table table-stripped table-condensed'>
    <thead>
        <th>Nom du document</th>
        <th>Généré par</th>
        <th>Date</th>
        <th class='text-right'>Actions</th>
    </thead>
    <tbody>
        % if template_history is not UNDEFINED and template_history:
            % for history in template_history:
                % if history.template is not None:
                    <tr>
                        <td>${history.template.description}</td>
                        <td>${api.format_account(history.user)}</td>
                        <td>${api.format_datetime(history.created_at)}</td>
                        <td class='text-right'>
                            <% url = request.route_path('/templatinghistory/{id}', id=history.id, _query=dict(action='delete')) %>
                            ${table_btn(url, \
                            u"Supprimer cette entrée",\
                            u"Supprimer cette entrée de l'historique", \
                            icon='trash', \
                            css_class="btn-danger")}
                        </td>
                    </tr>
                % endif
            % endfor
        % else:
            <tr><td colspan='4'>Aucun document n'a été généré</td></tr>
        % endif
    </tbody>
</table>
</%block>
