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
    invoice template
</%doc>
<%inherit file="/tasks/task.mako" />
<%namespace file="/base/utils.mako" import="format_text" />
<%def name="table(title, datas)">
    <div class="title">
        ${title}
    </div>
    <div class='content'>
        ${format_text(datas)}
    </div>
</%def>
<%block name='header'>
        <style>
            @page {
                size: a4 portrait;
                margin:1cm;
                margin-bottom:3.5cm;
                % if not task.has_been_validated() and not task.is_paid():
                    background-image: url("${request.static_url('autonomie:static/watermark_invoice.jpg', _app_url='')}");
                % endif
                @frame footer {
                    -pdf-frame-content: footer;
                    bottom: 0cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    height:3cm;
                }
            }
        </style>
</%block>
        <%block name='information'>
        <strong>Avoir N°</strong>${request.config.get('invoiceprefix')}${task.officialNumber}<br />
        <strong>Libellé : </strong>${task.number}<br />
        % if task.invoice:
            <span  style='color:#999'> <strong style='color:#999'>Référence facture N°</strong>${request.config.get('invoiceprefix')}${task.invoice.officialNumber} (${task.invoice.number})</span> <br />
                <br />
            % endif
            <strong>Objet : </strong>${format_text(task.description)}<br />
        </%block>
        <%block name="notes_and_conditions">
        %if task.reimbursementConditions:
            ${table(u"Conditions de remboursement", task.reimbursementConditions)}
        % endif
        % if config.has_key('coop_reimbursement'):
            ${table(u"Mode de remboursement", config['coop_reimbursement'])}
        %endif
        </%block>
