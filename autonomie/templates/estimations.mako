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
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='content'>
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
<% columns = 8 %>
    <div class='row'>
        <div class='col-md-4 col-md-offset-8 col-xs-12'>
            <table class='table table-bordered status-table'>
                <tr>
                    <td class='geninv-True'><br /></td>
                    <td>Devis concrétisés en facture</td>
                </tr>
                <tr>
                    <td class='signed-status-signed'><br /></td>
                    <td>Devis signés</td>
                </tr>
                <tr>
                    <td class=''><br /></td>
                    <td>Devis en cours</td>
                </tr>
                <tr>
                    <td class='signed-status-aborted'><br /></td>
                    <td>Devis annulés</td>
                </tr>
            </table>
        </div>
    </div>
    <table class="table table-condensed table-bordered status-table">
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
                % for id_, name, internal_number, status, signed_status, geninv, date, description, ht, tva, ttc, customer_id, customer_name, company_id, company_name in records:
                    <tr class="status status-${status} signed-status-${signed_status} geninv-${geninv}">
                        <td class="status-td">
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
                    <a href="${request.route_path('/estimations/{id}.html', id=id_)}"
                    title="Voir le document">
                    ${name} (<small>${internal_number}</small>)
                    </a>
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
                         href="${request.route_path('/estimations/{id}.pdf', id=id_)}"
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
    </div>
</div>
</%block>
