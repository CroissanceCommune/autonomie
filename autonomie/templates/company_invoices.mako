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
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_customer" />
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    </li>
    <li>
    </li>
</ul>
<div class='row'>
    <div class='span7'>
        <form class='form-search form-horizontal' id='search_form' method='GET'>
            <div style="padding-bottom:3px">
                <select id='customer-select' name='customer_id' data-placeholder="Sélectionner un client">
                    <option value='-1'></option>
                    %for customer in customers:
                        %if customer.id == customer_id:
                            <option selected='1' value='${customer.id}'>${customer.name} (${customer.code})</option>
                        %else:
                            <option value='${customer.id}'>${customer.name} (${customer.code})</option>
                        %endif
                    %endfor
                </select>
                <select name='year' id='year-select' class='span2' data-placeholder="Sélectionner une année">
                    %for year_option in years:
                        %if unicode(year) == unicode(year_option):
                            <option selected="1" value='${year_option}'>${year_option}</option>
                        %else:
                            <option value='${year_option}'>${year_option}</option>
                        %endif
                    %endfor
                </select>
                <select name='status' id='paid-select'>
                    %for label, value in status_options:
                        %if value == status:
                            <option selected="1" value='${value}'>${label}</option>
                        %else:
                            <option value='${value}'>${label}</option>
                        %endif
                    %endfor
                </select>
                <select class='span1' name='items_per_page'>
                    % for label, value in items_per_page_options:
                        % if int(value) == int(items_per_page):
                            <option value="${value}" selected='true'>${label}</option>
                        %else:
                            <option value="${value}">${label}</option>
                        %endif
                    % endfor
                </select>
            </div>
            <div class='pull-left' style="padding-right:3px">
                <input type='text' name='search' class='input-medium search-query' value="${search}" />
                <span class="help-block">Identifiant du document</span>
            </div>
            <button type="submit" class="btn btn-primary">Filtrer</button>
        </form>
    </div>
    <div class='span4'>
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
<table class="table table-condensed table-bordered">
    <thead>
        <th><span class="ui-icon ui-icon-comment"></span></th>
        <th>${sortable(u"Identifiant", "officialNumber")}</th>
        <th>${sortable(u"Émise le", 'taskDate')}</th>
        <th>${sortable(u"Nom de la facture", 'number')}</th>
        <th>${sortable(u"Client", 'customer')}</th>
        <th>Montant HT</th>
        <th>TVA</th>
        <th>TTC</th>
        <th>Information de paiement</th>
        <th>PDF</th>
    </thead>
    <tbody>
        <% totalht = sum([document.total_ht() for document in records]) %>
        <% totaltva = sum([document.tva_amount() for document in records]) %>
        <% totalttc = sum([document.total() for document in records]) %>
        <tr>
            <td colspan='5'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
        ## records are : Invoices, ManualInvoices or CancelInvoices
     % if records:
     % for document in records:
     % if document.is_cancelled():
        <tr class='invoice_cancelled_tr'>
            <td class='invoice_cancelled'>
                <span class="label label-important">
                    <i class="icon-white icon-remove"></i>
                </span>
     % elif document.is_tolate():
        <tr class='invoice_tolate_tr'>
            <td class='invoice_tolate'>
                <br />
     % elif document.is_paid():
        <tr class='invoice_paid_tr'>
            <td class='invoice_paid'>
     % elif document.is_resulted():
        <tr class='invoice_resulted_tr'>
            <td class='invoice_resulted'>
     % else:
         <tr>
             <td class='invoice_notpaid'>
                 <br />
     % endif
     %if document.statusComment:
         <span class="ui-icon ui-icon-comment" title="${document.statusComment}"></span>
     %endif
             </td>
             <td>
                 ${document.officialNumber}
             </td>
             <td>
                 ${api.format_date(document.taskDate)}
             </td>
             <td>
                <blockquote>
                    %if document.is_viewable():
                        <a href="${request.route_path(document.type_, id=document.id)}"
                            title='Voir le document'>${document.number}</a>
                    %else:
                        ${document.number}
                    %endif
                    <small>${format_text(document.description)}
                </blockquote>
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
             <td>
                 % if len(document.payments) == 1 and document.is_resulted():
                     Le ${api.format_date(document.payments[0].date)} (${api.format_paymentmode(document.payments[0].mode)})
                 % elif len(document.payments) > 0:
                     <ul>
                         % for payment in document.payments:
                             <li>
                                 ${api.format_amount(payment.amount)|n}&nbsp;€ le ${api.format_date(payment.date)} (${api.format_paymentmode(payment.mode)})
                             </li>
                         % endfor
                     </ul>
                 % endif

              </td>
              <td>
                  % if document.is_viewable():
                      <a class='btn'
                          href='${request.route_path(document.type_, id=document.id, _query=dict(view="pdf"))}'
                          title="Télécharger la version PDF">
                          <i class='icon icon-file'></i>
                      </a>
                  % endif
              </td>
          </tr>
      % endfor
  % else:
      <tr>
          <td colspan='10'>
              Aucune facture n'a pu être retrouvée
          </td>
      </tr>
  % endif
  </tbody>
  <tfoot>
      <tr>
          <td colspan='5'><strong>Total</strong></td>
          <td><strong>${api.format_amount(totalht)|n}&nbsp;€</strong></td>
          <td><strong>${api.format_amount(totaltva)|n}&nbsp;€</strong></td>
          <td><strong>${api.format_amount(totalttc)|n}&nbsp;€</strong></td>
          <td colspan='2'></td>
      </tr>
  </tfoot>
</table>
${pager(records)}
</%block>
<%block name='footerjs'>
$('#customer-select').chosen({allow_single_deselect: true});
$('#customer-select').change(function(){$(this).closest('form').submit()});
$('#year-select').chosen({allow_single_deselect: true});
$('#year-select').change(function(){$(this).closest('form').submit()});
$('#paid-select').chosen({allow_single_deselect: true});
$('#paid-select').change(function(){$(this).closest('form').submit()});
</%block>
