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
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    <a href='#filter-form'
        data-toggle='collapse'
        aria-expanded="false"
        aria-controls="filter-form">
        <i class='glyphicon glyphicon-search'></i>&nbsp;
        Filtres&nbsp;
        <i class='glyphicon glyphicon-chevron-down'></i>
    </a>
    % if '__formid__' in request.GET:
        <div class='help-text'>
            <small><i>Des filtres sont actifs</i></small>
        </div>
        <div class='help-text'>
            <a href="${request.current_route_path(_query={})}">
                <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
            </a>
        </div>
    % endif
    </div>
    <div class='panel-body'>
    % if '__formid__' in request.GET:
        <div class='collapse' id='filter-form'>
    % else:
        <div class='in collapse' id='filter-form'>
    % endif
            <div class='row'>
                <div class='col-xs-12'>
                    ${form|n}
                </div>
            </div>
        </div>
    </div>
</div>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    ${records.item_count} Résultat(s)
    </div>
    <div class='panel-body'>
        <div class='alert alert-info'>
            Vous trouverez ci-dessous la liste des fichiers comptables traités par Autonomie.
            <br />
            Lors du dépôt d'un fichier:
            <ul>
            <li>
            Le fichier est traité par un automate en "tâche de fond"
            </li>
            <li>
            Après l'import, des indicateurs sont générés depuis les écritures et en fonction de la configuration <br />
            <a
                class='link'
                onclick="window.openPopup('/admin/accounting/treasury_measures');"
                href='#'>
                Configuration-> Configuration du module Fichiers comptables -> Configuration des indicateurs de trésorerie
            </a>&nbsp;Pour les États de trésorerie (générés depuis la balance analytique)<br />
            <a
                class='link'
                onclick="window.openPopup('/admin/accounting/income_statement_measures');"
                href='#'>
                Configuration-> Configuration du module Fichiers comptables -> Configuration des indicateurs de compte de résultat
            </a>&nbsp;Pour les Comptes de résultat (générés depuis le grand livre)
            </li>
            </ul>
            <br />
            <b>Si une erreur s'est produite</b> : vous devriez avoir reçu un mail à l'adresse
            d'administration configurée dans
                <a
                class='link'
                href="#"
                onclick="window.openPopup('/admin/main');">
                    Configuration -> Configuration générale
                </a>
            <br />
            <br />
            <b>Si l'import s'est déroulé avec succès</b> : vous trouverez ici les informations relatives aux données importées.<br />
            <br />
            Vous pouvez :
            <ul>
                <li>Supprimer les données importées et les indicateurs associés si une erreur s'est produite (données mal associées par exemple)</li>
                <li>Recalculer les indicateurs issus du dernier import si vous avez modifié la configuration des indicateurs</li>
            </ul>
        </div>
    </div>
<table class="table table-striped table-condensed table-hover">
    <thead>
        <tr>
            <th>Type du fichier</th>
            <th class="visible-lg">${sortable(u"Traité le", "created_at")}</th>
            <th class="visible-lg">${sortable(u"Date d'export", "date")}</th>
            <th>${sortable(u"Nom du fichier", "filename")}</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for entry in records:
                <tr class='tableelement' id='${entry.id}'>
                    <td>
                        <i class='fa fa-book'></i> ${entry.filetype_label}
                    </td>
                    <td>${api.format_datetime(entry.created_at)}</td>
                    <td>${api.format_date(entry.date)}</td>
                    <td>
                        ${entry.filename}
                    </td>
                    <td class='actions'>
                    ${request.layout_manager.render_panel('action_dropdown', links=stream_actions(entry))}
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='5'>
                    Aucun fichier n'a été traité
                </td>
            </tr>
    % endif
    </tbody>
    </table>
${pager(records)}
</div>
</div>
</%block>
