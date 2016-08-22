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


<table class="table table-condensed table-bordered">
    <thead>
        <% num_columns = 11 %>
        <th><span class="glyphicon glyphicon-comment"></span></th>
        <th>${sortable(u"Identifiant", "official_number")}</th>
    % if is_admin_view:
        <% num_columns += 1 %>
        <th>${sortable(u"Entrepreneur", 'company')}</th>
    % endif
        <th>${sortable(u"Émise le", 'date')}</th>
        <th>${sortable(u"Nom de la facture", 'internal_number')}</th>
        <th>${sortable(u"Client", 'customer')}</th>
        <th>${sortable(u"Montant HT", "ht")}</th>
        <th>${sortable(u"TVA", "ht")}</th>
        <th>${sortable(u"TTC", "ttc")}</th>
        <th>${sortable(u"Paiement", "payment")}</th>
        <th>PDF</th>
        <th>Fichiers attachés</th>
    </thead>
    <tbody>
        <tr>
            <td colspan='${num_columns - 6}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc, precision=5)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
        ## invoices are : Invoices, ManualInvoices or CancelInvoices
        % if records:
            % for document in records:
                <% id_ = document.id %>
                <% description = document.description %>
                <% internal_number = document.internal_number %>
                <% ht = document.ht %>
                <% tva = document.tva %>
                <% ttc = document.ttc %>
                <% status = document.CAEStatus %>
                <% date = document.date %>
                <% type_ = document.type_ %>
                <% prefix = document.prefix %>
                <% official_number = document.official_number %>
                % if is_admin_view:
                    <% company = document.get_company() %>
                    <% company_id = company.id %>
                    <% company_name = company.name %>
                % endif
                <% customer_id = document.customer.id %>
                <% customer_name = document.customer.name %>

                % if type_ == 'cancelinvoice' or status == 'resulted':
                    <tr class='invoice_resulted_tr'>
                        <td class='invoice_resulted'>
                        </td>
                % elif invoice_tolate(date, status):
                    <tr class='invoice_tolate_tr'>
                        <td class='invoice_tolate'>
                        </td>
                % elif status == 'paid':
                    <tr class='invoice_paid_tr'>
                        <td class='invoice_paid'>
                        </td>
                % else:
                    <tr>
                        <td class='invoice_notpaid'>
                            <br />
                        </td>
                % endif
            <td>
                ${prefix}${official_number}
            </td>
            % if is_admin_view:
                <td>
                    <a
                        href="${request.route_path('company', id=company_id)}"
                        title="Voir l'entreprise">
                        ${company_name}
                    </a>
                </td>
            % endif
            <td>
                ${api.format_date(date)}
            </td>
            <td>
                <a href="${request.route_path(document.type_, id=id_)}"
                    title='Voir le document'>
                    ${internal_number}
                </a>
                % if not is_admin_view:
                <small>
                    ${format_text(description)}
                </small>
                % endif
            </td>
            <td class='invoice_company_name'>
                <a href="${request.route_path("customer", id=customer_id)}">
                    ${customer_name}
                </a>
            </td>
            <td>
                <strong>${api.format_amount(ht, precision=5)|n}&nbsp;€</strong>
            </td>
            <td>
                ${api.format_amount(tva, precision=5)|n}&nbsp;€
            </td>
            <td>
                ${api.format_amount(ttc, precision=5)|n}&nbsp;€
            </td>
            <td>
                % if len(document.payments) == 1 and status == 'resulted':
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
                                    ${api.format_amount(payment.amount, precision=5)|n}&nbsp;€
                                    le ${api.format_date(payment.date)}
                                    (${api.format_paymentmode(payment.mode)})
                                </a>
                            </li>
                        % endfor
                    </ul>
                % endif
            </td>
            <td>
                <a class='btn btn-default'
                    href='${request.route_path(document.type_, id=document.id, _query=dict(view="pdf"))}'
                    title="Télécharger la version PDF">
                    <i class='glyphicon glyphicon-file'></i>
                </a>
            </td>
              <td>
                  ${format_filelist(document)}
                  % if hasattr(document, 'estimation') and document.estimation_id is not None:
                    ${format_filelist(document.estimation)}
                % elif hasattr(document, 'invoice') and document.invoice_id is not None:
                    ${format_filelist(document.invoice)}
                  % endif
                  <a class='btn btn-default'
                      href='${request.route_path(document.type_, id=document.id, _query=dict(action="attach_file"))}'
                      title="Attacher un fichier">
                      <i class='glyphicon glyphicon-plus'></i>
                  </a>
              </td>
        </tr>
        % endfor
    % else:
        <tr>
            <td colspan='${num_columns}'>
                Aucune facture n'a pu être retrouvée
            </td>
        </tr>
    % endif
    </tbody>
    <tfoot>
        <tr>
            <td colspan='${num_columns - 6}'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva, precision=5)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc, precision=5)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
    </tfoot>
</table>
