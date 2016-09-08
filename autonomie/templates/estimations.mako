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

    Estimation list page
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='actionmenu'>
<div class='row'>
    <div class='col-md-7'>
        ${form|n}
    </div>
    <div class='col-md-4'>
        <table class='table table-bordered'>
            <tr>
                <td class='estimation_geninv'><br /></td>
                <td>Devis concrétisés en facture</td>
            </tr>
            <tr>
                <td class='estimation_valid'><br /></td>
                <td>Devis en cours</td>
            </tr>
            <tr>
                <td class='estimation_aboest'><br /></td>
                <td>Devis annulés</td>
            </tr>
        </table>
    </div>
</%block>
<%block name='content'>
<% columns = 8 %>

<table class="table table-condensed table-bordered">
    <thead>
        <th><span class="ui-icon ui-icon-comment"></span></th>
        % if is_admin:
            <% columns += 1 %>
            <th>${sortable(u"Entrepreneur", 'company')}</th>
        % endif
        <th>${sortable(u"Émis le", 'date')}</th>
        <th>Description</th>
        <th>${sortable(u"Client", 'customer')}</th>
        <th>Montant HT</th>
        <th>TVA</th>
        <th>TTC</th>
        <th class="actions">PDF</th>
    </thead>
    <tbody>
        <tr>
            <td colspan='${columns - 4}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc, precision=5)|n}&nbsp;€</strong></td>
            <td colspan='1'></td>
        </tr>
        % if records:
            % for id_, name, internal_number, CAEStatus, date, description, ht, tva, ttc, customer_id, customer_name, company_id, company_name in records:
                <tr class="estimation_${CAEStatus}_tr">
                    <td class="estimation_${CAEStatus}">
                    </td>
            % if is_admin:
                <td class='invoice_company_name'>
                    <a href="${request.route_path("company", id=company_id)}">
                        ${company_name}
                    </a>
                </td>
            % endif
            <td>${api.format_date(date)}</td>
            <td>
                <a href="${request.route_path("estimation", id=id_)}" title="Voir le document">${name} (<small>${internal_number}</small>)</a>
                <small>${format_text(description)}</small>
            </td>
            <td>
                <a href="${request.route_path("customer", id=customer_id)}">
                    ${customer_name}
                </a>
            </td>
             <td>
                 <strong>
                    ${api.format_amount(ht, precision=5) | n}&nbsp;€
                 </strong>
             </td>
             <td>
                 ${api.format_amount(tva, precision=5) | n}&nbsp;€
             </td>
             <td>
                 ${api.format_amount(ttc, precision=5) | n}&nbsp;€
             </td>
             <td class="actions">
                 <a class='btn btn-default'
                     href='${request.route_path("estimation", id=id_, _query=dict(view="pdf"))}'
                     title="Télécharger la version PDF">
                     <i class='glyphicon glyphicon-file'></i>
                 </a>
              </td>
          </tr>
      % endfor
        <tr>
            <td colspan='${columns - 4}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc, precision=5)|n}&nbsp;€</strong></td>
            <td colspan='1'></td>
        </tr>
  % else:
      <tr>
          <td colspan='7'>
              Aucun devis n'a pu être retrouvé
          </td>
      </tr>
  % endif
  </tbody>
</table>
${pager(records)}
</%block>
