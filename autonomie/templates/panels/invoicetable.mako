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
        <th>${sortable(u"Nom de la facture", 'number')}</th>
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
            <td><strong>${api.format_amount(totalht)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
        ## invoices are : Invoices, ManualInvoices or CancelInvoices
        % if records:
            % for document in records:
                % if document.is_tolate():
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
                ${document.prefix}${document.official_number}
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
                ${api.format_date(document.date)}
            </td>
            <td>
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
            </td>
            <td class='invoice_company_name'>
                ${format_customer(document.get_customer())}
            </td>
            <td>
                <strong>${api.format_amount(document.ht)|n}&nbsp;€</strong>
            </td>
            <td>
                ${api.format_amount(document.tva)|n}&nbsp;€
            </td>
            <td>
                ${api.format_amount(document.ttc)|n}&nbsp;€
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
                    <a class='btn btn-default'
                        href='${request.route_path(document.type_, id=document.id, _query=dict(view="pdf"))}'
                        title="Télécharger la version PDF">
                        <i class='glyphicon glyphicon-file'></i>
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
            <td><strong>${api.format_amount(totalht)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)|n}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totalttc)|n}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
    </tfoot>
</table>
