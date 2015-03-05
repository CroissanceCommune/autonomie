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
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    % if is_admin:
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
        <table class='table table-bordered'>
            <tr>
                <td class='invoice_resulted'><br /></td>
                <td>Factures payées</td>
            </tr>
            <tr>
                <td class='invoice_paid'><br /></td>
                <td>Factures payées partiellement</td>
            </tr>
            <tr>
                <td class='invoice_notpaid'><br /></td>
                <td>Factures non payées depuis moins de 45 jours</td>
            </tr>
            <tr>
                <td class='invoice_tolate'><br /></td>
                <td>Factures non payées depuis plus de 45 jours</td>
            </tr>
        </table>
    </div>
</div>
</%block>
<%block name='content'>
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
