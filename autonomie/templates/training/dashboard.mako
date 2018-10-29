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
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Liens utiles
    </div>
    <div class='panel-body'>
        % for link in trainer_datas_links:
        ${request.layout_manager.render_panel('link', context=link)}
        % endfor
    </div>
</div>
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
    <table class="table table-condensed table-bordered">
        <thead>
            <th>Statut</th>
            <th>Intitulé de la formation</th>
            <th>Enseigne</th>
            <th>Client</th>
            <th class='text-right'>Actions</th>
        </thead>
        <tbody>
        % if records:
            % for id_, record in records:
                <tr>
                    % for column in stream_columns(record):
                    <td>${column | n}</td>
                    % endfor
                    <td class='text-right'>
                    ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(record))}
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
            <td colspan="4"><em>Aucun élément n'a été retrouvé</em></td>
            </tr>
        % endif
        </tbody>
    </table>
    ${pager(records)}
    </div>
</div>
</%block>
