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
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='afteractionmenu'>
    <div class="alert alert-info">
        <i class='fa fa-help'></i>
        Configuration des modèles statistiques:
        <ul>
            <li>Créer une feuille de statistiques</li>
            <li>Composer vos entrées statistiques à l'aide de un ou plusieurs critères</li>
            <li>Générer les fichiers de sorties</li>
        </ul>
    </div>
<div class='page-header-block'>
        <button class='btn btn-success btn-add'
        title="Créer une nouvelle feuille de statistiques"
    >
        Ajouter
        </button>
        <div style="display:none" id='form-container'>
        </div>
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
<div class='panel-heading'>
Feuilles de statistiques
</div>
<div class='panel-body'>
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
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
                <% icon = sheet.active and u'remove' or '' %>
                <% css_class = sheet.active and u'btn-danger' or 'btn-success' %>
                ${table_btn(url, label, u"Ce modèle est-il toujours utilisé ?", icon=icon, css_class=css_class)}
                % if not sheet.active:
                    <% url = request.route_path('statistic', id=sheet.id, _query=dict(action='delete')) %>
                    <% label = u"Supprimer" %>
                    ${table_btn(url, label, u"Définitivement supprimer ce modèle ?", icon=u"remove", css_class="btn-danger")}
                % endif
            </td>
        </tr>
    % endfor
    </tbody>
    </table>
    </div>
</div>
    </div>
</div>
</%block>
<%block name='footerjs'>
AppOptions = {};
AppOptions['submiturl'] = "${submiturl}";
</%block>
