<%doc>
    * Copyright (C) 2012-2015 Croissance Commune
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
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='content'>
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
    <div class='well'>
        <button class='btn btn-success btn-add'
        title="Créer une nouvelle feuille de statistiques"
    >
        Ajouter
        </button>
        <div style="display:none" id='form-container'>
        </div>
    </div>
    <div class="alert alert-danger">
        <i class='fa fa-warning'></i>
        Configuration des modèles statistiques:
        <ul>
            <li>Créer une feuille de statistiques</li>
            <li>Composer vos entrées statistiques à l'aide de un ou plusieurs critères</li>
            <li>Générer les fichiers de sorties</li>
        </ul>
    </div>
    <table class='table table-stripped table-condensed'>
    <thead>
        <th> Nom de la feuille de statistiques </th>
        <th> Modifiée le </th>
        <th style="text-align:right"> Actions </th>
    </thead>
    <tbody>
    % for sheet in sheets:
        <tr
            % if not sheet.active:
                style="text-decoration: line-through;"
            % endif
            >
            <td>${sheet.title}</td>
            <td>${api.format_date(sheet.updated_at)}</td>
            <td style="text-align:right">
                <% url = request.route_path('statistic', id=sheet.id) %>
                ${table_btn(url, u"Voir/Modifier", u"Voir cette feuille", icon=u"pencil")}
                <% url = request.route_path('statistic', id=sheet.id, _query=dict(action='duplicate')) %>
                ${table_btn(url, u"Dupliquer", u"Dupliquer cette feuille", icon=u"tags")}
                <% url = request.route_path('statistic', id=sheet.id, _query=dict(action='disable')) %>
                <% label = sheet.active and u"Désactiver" or u"Activer" %>
                ${table_btn(url, label, u"Ce modèle est-il toujours utilisé ?", icon=u"remove", css_class="btn-danger")}
            </td>
        </tr>
    % endfor
    </tbody>
    </table>
    </div>
</div>
</%block>
<%block name='footerjs'>
AppOptions = {};
AppOptions['submiturl'] = "${submiturl}";
</%block>
