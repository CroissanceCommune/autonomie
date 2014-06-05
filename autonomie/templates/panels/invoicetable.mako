<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
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
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="format_text"/>
<%namespace file="/base/utils.mako" import="format_customer"/>
<%namespace file="/base/utils.mako" import="format_filelist" />

<%
totalht = sum([invoice.total_ht() for invoice in records])
totaltva = sum([invoice.tva_amount() for invoice in records])
totalttc = sum([invoice.total() for invoice in records])
if is_admin_view:
    columns = 12
else:
    columns = 11
%>

<table class="table table-condensed table-bordered">
    <thead>
        <th><span class="ui-icon ui-icon-comment"></span></th>
        <th>${sortable(u"Identifiant", "officialNumber")}</th>
    % if is_admin_view:
        <th>${sortable(u"Entrepreneur", 'company')}</th>
    % endif
        <th>${sortable(u"Émise le", 'taskDate')}</th>
        <th>${sortable(u"Nom de la facture", 'number')}</th>
        <th>${sortable(u"Client", 'customer')}</th>
        <th>Montant HT</th>
        <th>TVA</th>
        <th>TTC</th>
        <th>Information de paiement</th>
        <th>PDF</th>
        <th>Fichiers attachés</th>
    </thead>
    <tbody>
        <tr>
            <td colspan='${columns - 6}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
        ## invoices are : Invoices, ManualInvoices or CancelInvoices
        % if records:
            % for document in records:
                %if document.is_cancelled():
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
                ${request.config.get('invoiceprefix')}${document.officialNumber}
            </td>
            % if is_admin_view:
            <td>
                <% company = document.get_company() %>
                % if company:
                    <a href="${request.route_path('company', id=company.id)}"
                        title="Voir l'entreprise">${company.name}</a>
                % endif
            </td>
            % endif
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
                    % if not is_admin_view:
                    <small>
                        ${format_text(document.description)}
                    </small>
                    % endif
                </blockquote>
            </td>
            <td class='invoice_company_name'>
                ${format_customer(document.get_customer())}
            </td>
            <td>
                <strong>${api.format_amount(document.total_ht())|n}&nbsp;€</strong>
            </td>
            <td>
                ${api.format_amount(document.tva_amount())|n}&nbsp;€
            </td>
            <td>
                ${api.format_amount(document.total())|n}&nbsp;€
            </td>
            <td>
                % if len(document.payments) == 1 and document.is_resulted():
                    <% payment = document.payments[0] %>
                    <% url = request.route_path('payment', id=payment.id) %>
                    <a href="${url}">
                    Le ${api.format_date(payment.date)}
                    (${api.format_paymentmode(payment.mode)})
                    </a>
                % elif len(document.payments) > 0:
                    <ul>
                        % for payment in document.payments:
                    <% url = request.route_path('payment', id=payment.id) %>
                            <li>
                                <a href="${url}">
                            ${api.format_amount(payment.amount)|n}&nbsp;€
                            le ${api.format_date(payment.date)}
                            (${api.format_paymentmode(payment.mode)})
                                </a>
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
                %endif
            </td>
              <td>
                  ${format_filelist(document)}
                  % if hasattr(document, 'estimation'):
                    ${format_filelist(document.estimation)}
                % elif hasattr(document, 'invoice'):
                    ${format_filelist(document.invoice)}
                  % endif
                  <a class='btn'
                      href='${request.route_path(document.type_, id=document.id, _query=dict(action="attach_file"))}'
                      title="Attacher un fichier">
                      <i class='icon icon-plus'></i>
                  </a>
              </td>
        </tr>
        % endfor
    % else:
        <tr>
            <td colspan='${columns}'>
                Aucune facture n'a pu être retrouvée
            </td>
        </tr>
    % endif
    </tbody>
    <tfoot>
        <tr>
            <td colspan='${columns - 6}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
    </tfoot>
</table>
