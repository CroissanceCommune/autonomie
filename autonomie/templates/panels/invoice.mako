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
    invoice panel template
</%doc>
<%inherit file="/panels/task.mako" />
<%namespace file="/base/utils.mako" import="format_text" />
<%def name="table(title, datas)">
    <div class="title">
        ${title}
    </div>
    <div class='content'>
        ${format_text(datas)}
    </div>
</%def>
<%block name='information'>
<strong>Facture N°</strong>${task.prefix}${task.official_number}<br />
<strong>Libellé : </strong>${task.internal_number}<br />
% if task.estimation is not None:
    <strong>Cette facture est associée au devis : </strong>${task.estimation.internal_number}<br />
% endif
<strong>Objet : </strong>${format_text(task.description)}<br />
% if task.workplace:
    <strong>Lieu d'éxécution des travaux : </strong>
    <br />
    ${format_text(task.workplace)}
    <br />
% endif
% if config.get('coop_invoiceheader'):
    ${format_text(config['coop_invoiceheader'])}
% endif
</%block>
<%block name="notes_and_conditions">
%if task.payment_conditions:
    ${table(u"Conditions de paiement", task.payment_conditions)}
% endif
% if config.get('coop_invoicepayment'):
    <% paymentinfo = config.get('coop_invoicepayment')%>
    % if company.IBAN is not None:
        <% paymentinfo = paymentinfo.replace(u"%IBAN%", company.IBAN) %>
    % endif
    % if company.RIB is not None:
        <% paymentinfo = paymentinfo.replace(u"%RIB%", company.RIB) %>
    % endif
    % if company.name is not None:
        <% paymentinfo = paymentinfo.replace(u"%ENTREPRENEUR%", company.name) %>
    % endif
    ${table(u"Mode de paiement", paymentinfo)}
%endif
% if config.get('coop_invoicelate'):
    <% tolate = config.get('coop_invoicelate').replace(u"%ENTREPRENEUR%", company.name) %>
    ${table(u"Retard de paiement", tolate)}
% endif
</%block>
