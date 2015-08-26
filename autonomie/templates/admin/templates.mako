<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
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
<%inherit file="/admin/index.mako"></%inherit>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='content'>
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
    <div class='well'>
        <a class='btn btn-success'
        href="${request.route_path('templates', _query=dict(action='new'))}"
        title="Téléverser un nouveau modèle de document"
    >
        Ajouter
    </a>
    </div>
    <div class="alert alert-danger">
        <i class='fa fa-warning'></i>
        Les modèles de document doivent être au format odt pour pouvoir être utilisés par Autonomie
    </div>
    <table class='table table-stripped table-condensed'>
    <thead>
        <th> Nom du fichier </th>
        <th> Description </th>
        <th> Déposé le </th>
        <th style="text-align:right"> Actions </th>
    </thead>
    <tbody>
    % for template in templates:
        <tr
            % if not template.active:
                style="text-decoration: line-through;"
            % endif
            >
            <td>${template.name}</td>
            <td>${template.description}</td>
            <td>${api.format_date(template.updated_at)}</td>
            <td style="text-align:right">
                <% url = request.route_path('template', id=template.id) %>
                ${table_btn(url, u"Voir", u"Voir ce modèle", icon=u"pencil")}
                <% url = request.route_path('template', id=template.id, _query=dict(action='edit')) %>
                ${table_btn(url, u"Modifier", u"Éditer ce modèle", icon=u"pencil")}
                <% url = request.route_path('template', id=template.id, _query=dict(action='disable')) %>
                <% label = template.active and u"Désactiver" or u"Activer" %>
                ${table_btn(url, label, u"Ce modèle doit-il être visible dans Autonomie ?", icon=u"remove")}
                % if not template.active:
                    <% url = request.route_path('template', id=template.id, _query=dict(action='delete')) %>
                    <% label = u"Supprimer" %>
                    ${table_btn(
                        url,
                        label,
                        u"Suppression définitive de ce modèle",
                        icon=u"trash",
                        onclick=u"return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');",
                        css_class="btn-danger")}
                % endif
            </td>
        </tr>
    % endfor
    </tbody>
    </table>
    </div>
</div>
</%block>
