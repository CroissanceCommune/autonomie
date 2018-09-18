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
<%block name='content'>
<div class='row page-header-block'>
    % if api.has_permission('admin_treasury'):
        <a
            class='btn btn-default primary-action'
            href='/invoices?action=export_pdf'>
            <i class='fa fa-file-pdf-o'></i>&nbsp;Export massif
        </a>
    % endif
    <div class="pull-right btn-group" role='group'>
        <%
## We build the link with the current search arguments
        args = request.GET
        if is_admin:
            url = request.route_path('invoices_export', extension="xls", _query=args)
        else:
            url = request.route_path('company_invoices_export', extension="xls", id=request.context.id, _query=args)
        %>
        <a
            class='btn btn-default'
            onclick="window.openPopup('${url}');"
            href='#'
            title="Export au format Excel"
            >
            <i class='fa fa-file-excel-o'></i> Excel
        </a>
        <%
## We build the link with the current search arguments
        args = request.GET
        if is_admin:
            url = request.route_path('invoices_export', extension="ods", _query=args)
        else:
            url = request.route_path('company_invoices_export', extension="ods", id=request.context.id, _query=args)
        %>
        <a
            class='btn btn-default'
            onclick="window.openPopup('${url}');"
            href='#'
            title="Export au formt Open document"
            >
            <i class='fa fa-file'></i> ODS
        </a>
        <%
## We build the link with the current search arguments
        args = request.GET
        if is_admin:
            url = request.route_path('invoices_export', extension="csv", _query=args)
        else:
            url = request.route_path('company_invoices_export', extension="csv", id=request.context.id, _query=args)
        %>
        <a
            class='btn btn-default'
            onclick="window.openPopup('${url}');"
            href='#'
            title="Export au formt csv"
            >
            <i class='fa fa-file'></i> CSV
        </a>
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
        ${request.layout_manager.render_panel('task_list', records, legends=legends, datatype="invoice", is_admin_view=is_admin)}
        ${pager(records)}
    </div>
</div>
</%block>
<%block name='footerjs'>
## #deformField2_chzn (company_id) and #deformField3_chzn (customer_id) are the
## tag names
% if is_admin:
    $('#deformField2_chzn').change(function(){$(this).closest('form').submit()});
% endif
$('#deformField3_chzn').change(function(){$(this).closest('form').submit()});
$('select[name=year]').change(function(){$(this).closest('form').submit()});
$('select[name=status]').change(function(){$(this).closest('form').submit()});
</%block>
