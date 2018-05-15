<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
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

<%doc>
    Invoice List for a given company
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/pager.mako" import="pager"/>
<%block name='mainblock'>
<div class='row page-header-block'>
    <div class="pull-right btn-group" role='group'>
        <%
## We build the link with the current search arguments
        args = request.GET
        url = request.route_path('/projects/{id}/invoices.{extension}', extension='xls', id=request.context.id, _query=args)
        %>
        <a
            class='btn btn-default btn-small'
            onclick="openPopup('${url}');"
            href='#'
            title="Export au format Excel"
            >
            <i class='fa fa-file-excel-o'></i> Excel
        </a>
        <%
## We build the link with the current search arguments
        args = request.GET
        url = request.route_path('/projects/{id}/invoices.{extension}', extension='ods', id=request.context.id, _query=args)
        %>
        <a
            class='btn btn-default btn-small'
            onclick="openPopup('${url}');"
            href='#'
            title="Export au formt Open document"
            >
            <i class='fa fa-file'></i> ODS
        </a>
        <%
## We build the link with the current search arguments
        args = request.GET
        url = request.route_path('/projects/{id}/invoices.{extension}', extension='csv', id=request.context.id, _query=args)
        %>
        <a
            class='btn btn-default btn-small'
            onclick="openPopup('${url}');"
            href='#'
            title="Export au formt csv"
            >
            <i class='fa fa-file'></i> CSV
        </a>
    </div>
</div>
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
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    ${records.item_count} Résultat(s)
    </div>
    <div class='panel-body'>
        <div class='row'>
            <div class='col-md-4 col-md-offset-8 col-xs-12'>
                <table class='table table-bordered status-table'>
                    <tr>
                        <td class='paid-status-resulted'><br /></td>
                        <td>Factures payées</td>
                    </tr>
                    <tr>
                        <td class='paid-status-paid'><br /></td>
                        <td>Factures payées partiellement</td>
                    </tr>
                    <tr>
                        <td class=''><br /></td>
                        <td>Factures non payées depuis moins de 45 jours</td>
                    </tr>
                    <tr>
                        <td class='tolate-True'><br /></td>
                        <td>Factures non payées depuis plus de 45 jours</td>
                    </tr>
                    <tr>
                        <td class='status-draft'><br /></td>
                        <td>Factures en brouillon</td>
                    </tr>
                    <tr>
                        <td class='status-wait'><br /></td>
                        <td>Factures en attente de validation</td>
                    </tr>
                    <tr>
                        <td class='status-invalid'><br /></td>
                        <td>Factures invalides</td>
                    </tr>
                </table>
            </div>
        </div>
        ${request.layout_manager.render_panel('invoicetable', records, is_admin_view=is_admin)}
        ${pager(records)}
    </div>
</div>
</%block>
