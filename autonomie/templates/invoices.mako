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
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    % if api.has_permission('admin_treasury'):
        ${pdf_export_btn.render(request)|n}
    % endif
    </li>
    <li>
    </li>
</ul>
<div class='row'>
    <div class='col-md-7'>
        ${form|n}
    </div>
    <div class='col-md-4'>
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
        </table>
    </div>
</div>
</%block>
<%block name='content'>
<div class="well well-sm pull-right btn-group" role='group'>
    <%
## We build the link with the current search arguments
    args = request.GET
    if is_admin:
        url = request.route_path('invoices.xls', _query=args)
    else:
        url = request.route_path('company_invoices.xls', id=request.context.id, _query=args)
    %>
    <a
        class='btn btn-default'
        href='${url}'
        title="Export au format Excel"
        target='_blank'
        >
        <i class='fa fa-file-excel-o'></i> Excel
    </a>
    <%
## We build the link with the current search arguments
    args = request.GET
    if is_admin:
        url = request.route_path('invoices.ods', _query=args)
    else:
        url = request.route_path('company_invoices.ods', id=request.context.id, _query=args)
    %>
    <a
        class='btn btn-default'
        href='${url}'
        title="Export au formt Open document"
        target='_blank'
        >
        <i class='fa fa-file'></i> ODS
    </a>
    <%
## We build the link with the current search arguments
    args = request.GET
    if is_admin:
        url = request.route_path('invoices.csv', _query=args)
    else:
        url = request.route_path('company_invoices.csv', id=request.context.id, _query=args)
    %>
    <a
        class='btn btn-default'
        href='${url}'
        title="Export au formt csv"
        target='_blank'
        >
        <i class='fa fa-file'></i> CSV
    </a>
</div>
${request.layout_manager.render_panel('invoicetable', records, is_admin_view=is_admin)}
${pager(records)}
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
