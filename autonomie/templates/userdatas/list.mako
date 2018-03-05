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
<%block name='afteractionmenu'>
<div class='page-header-block'>
            <a
                class='btn btn-primary primary-action'
                href="${request.route_path('/userdatas', _query=dict(action='add'))}">
                Nouvelle entrée gestion sociale
            </a>
        % if api.has_permission('admin'):
            <a
                class='btn btn-default secondary-action'
                href="${request.route_path('import_step1')}">
                Importer des données
            </a>
        % endif
    <div class='pull-right btn-group' role='group'>
            <%
        args = request.GET
        url = request.route_path('/userdatas.xls', _query=args)
        %>
        <a
            class='btn btn-default'
            href='#'
            onclick="openPopup('${url}');"
            title="Exporter les éléments de la liste au format xls">
            <i class='fa fa-file-excel-o'></i>&nbsp;Excel
        </a>
            <%
        args = request.GET
        url = request.route_path('/userdatas.ods', _query=args)
        %>
        <a
            class='btn btn-default'
            href='#'
            onclick="openPopup('${url}');"
            title="Exporter les éléments de la liste au format ods">
            <i class='fa fa-file'></i>&nbsp;ODS
        </a>
            <%
        args = request.GET
        url = request.route_path('/userdatas.csv', _query=args)
        %>
        <a
            class='btn btn-default'
            href='#'
            onclick="openPopup('${url}');"
            title="Exporter les éléments de la liste au format csv">
            <i class='fa fa-file'></i>&nbsp;CSV
        </a>
    </div>
</div>
</%block>
<%block name="content">
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
<table class="table table-condensed table-hover">
    <thead>
        <tr>
            <th>${sortable("Nom", "lastname")}</th>
            <th>Accompagnateur</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % for userdata in records:
            <% url = request.route_path('/users/{id}/userdatas/edit', id=userdata.user_id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <% css = "white_" %>
            <tr class='${css}tr'>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(userdata)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(userdata.situation_follower)}
                </td>
                <td class="actions">
                    <div class='btn-group'>
                        <button
                            type="button"
                            class="btn btn-default dropdown-toggle"
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false">
                            Actions <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-right">
                            % for url, label, title, icon, options in stream_actions(userdata):
                                ${dropdown_item(url, label, title, icon=icon, **options)}
                            % endfor
                        </ul>
                    </div>
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</div>
</div>
</%block>
