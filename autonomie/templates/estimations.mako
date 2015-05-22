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
<%namespace file="/base/utils.mako" import="format_customer" />
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
<table class="table table-condensed table-bordered">
    <thead>
        <th><span class="ui-icon ui-icon-comment"></span></th>
        <th>${sortable(u"Émis le", 'taskDate')}</th>
        <th>Description</th>
        <th>${sortable(u"Client", 'customer')}</th>
        <th>Montant HT</th>
        <th>TVA</th>
        <th>TTC</th>
        <th class="actions">PDF</th>
    </thead>
    <tbody>
        % if records:
            % for document in records:
                <tr class="estimation_${document.CAEStatus}_tr">
                    <td class="estimation_${document.CAEStatus}">
                %if document.statusComment:
                    <span class="ui-icon ui-icon-comment" title="${document.statusComment}"></span>
                %endif
            </td>
            <td>${api.format_date(document.taskDate)}</td>
            <td>
                <a href="${request.route_path("estimation", id=document.id)}" title="Voir le document">${document.name}</a>
                <small>${format_text(document.description)}</small>
            </td>
            <td class='invoice_company_name'>
                ${format_customer(document.get_customer())}
            </td>
             <td>
                 <strong>
                    ${api.format_amount(document.total_ht())|n}&nbsp;€
                 </strong>
             </td>
             <td>
                 ${api.format_amount(document.tva_amount())|n}&nbsp;€
             </td>
             <td>
                 ${api.format_amount(document.total())|n}&nbsp;€
             </td>
             <td class="actions">
                      <a class='btn btn-default'
                          href='${request.route_path("estimation", id=document.id, _query=dict(view="pdf"))}'
                          title="Télécharger la version PDF">
                          <i class='glyphicon glyphicon-file'></i>
                      </a>
              </td>
          </tr>
      % endfor
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
