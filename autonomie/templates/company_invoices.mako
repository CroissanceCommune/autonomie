<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_client" />
<%block name='actionmenu'>
<style>
    .invoice_paid{
        background-color:#fff866;
        width:36px;
        }
    .invoice_notpaid{
        background-color:#ffffff;
        width:36px;
    }
    .invoice_tolate{
    background-color:#C43C35;
        width:36px;
    }
    .invoice_tolate a{
    color:#fff;
        text-transform:uppercase;
        text-decoration:underline;
    }
   .invoice_tolate_tr{
      background-color:#f9aaaa;
      }
      .invoice_paid_tr{
      background-color:#fffbaa;
    }
    .invoice_cancelled_tr{
        background-color:#eeeeee;
        }
</style>
<ul class='nav nav-pills'>
    <li>
    </li>
    <li>
    </li>
</ul>
<div class='row'>
    <div class='span7'>
        <form class='navbar-form form-search form-horizontal' id='search_form' method='GET'>
            <div style="padding-bottom:3px">
            <select id='client-select' name='client' data-placeholder="Sélectionner un client">
                <option value=''></option>
                %for client in company.clients:
                    %if client.id == current_client:
                        <option selected='1' value='${client.id}'>${client.name} (${client.id})</option>
                    %else:
                        <option value='${client.id}'>${client.name} (${client.id})</option>
                    %endif
                %endfor
            </select>
            <select name='year' id='year-select' class='span2' data-placeholder="Sélectionner une année">
                %for year in years:
                    %if unicode(current_year) == unicode(year):
                        <option selected="1" value='${year}'>${year}</option>
                    %else:
                        <option value='${year}'>${year}</option>
                    %endif
                %endfor
            </select>
            <select name='paid' id='paid-select'>
                %for value, label in (('both', u"Toutes les factures"), ("paid", u"Les factures payées"), ("notpaid", u"Seulement les impayés")):
                    %if current_paid == value:
                        <option selected="1" value='${value}'>${label}</option>
                    %else:
                        <option value='${value}'>${label}</option>
                    %endif
                %endfor
            </select>
            <select class='span1' name='nb'>
                % for text, value in (('10 par page', u'10'), ('20 par page', u'20'), ('30 par page', u'30'), ("40 par page", u'40'), ('50 par page', u'50'), ('Tous', u'10000'),):
                    <% nb_item = request.GET.get("nb") %>
                    % if nb_item == value or request.cookies.get('items_per_page') == value:
                        <option value="${value}" selected='true'>${text}</option>
                    %else:
                        <option value="${value}">${text}</option>
                    %endif
                % endfor
            </select>
            </div>
            <div class='floatted' style="padding-right:3px">
                    <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}" />
                    <span class="help-block">Identifiant du document</span>
            </div>
            <button type="submit" class="btn btn-primary">Filtrer</button>
        </form>
    </div>
    <div class='span4'>
        <table class='table table-bordered'>
            <tr>
                <td class='invoice_paid'><br /></td>
                <td>Factures payées</td>
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
        <th>${sortable(u"Client", 'client')}</th>
        <th>Montant HT</th>
        <th>TVA</th>
        <th>Information de paiement</th>
        <th>PDF</th>
    </thead>
    <tbody>
        <% totalht = sum([invoice.total_ht() for invoice in invoices]) %>
        <% totaltva = sum([invoice.tva_amount() for invoice in invoices]) %>
        <tr>
            <td colspan='5'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht)}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
        ## invoices are : Invoices, ManualInvoices or CancelInvoices
        % if invoices:
            % for invoice in invoices:
                % if invoice.is_invoice():
                    <% route_name="invoice" %>
                % else:
                    <% route_name="cancelinvoice" %>
                %endif
                    %if invoice.is_invoice() and invoice.is_cancelled():
                        <tr class='invoice_cancelled_tr'>
                            <td class='invoice_cancelled'>
                                <span class="label label-important">
                                    <i class="icon-white icon-remove"></i>
                                </span>
                    % elif invoice.is_tolate():
                        <tr class='invoice_tolate_tr'>
                            <td class='invoice_tolate'>
                                <br />
                    % elif invoice.is_paid():
                        <tr class='invoice_paid_tr'>
                            <td class='invoice_paid'>
                    % else:
                        <tr>
                            <td class='invoice_notpaid'>
                                <br />
                    % endif
                    %if hasattr(invoice, "statusComment") and invoice.statusComment:
                        <span class="ui-icon ui-icon-comment" title="${invoice.statusComment}"></span>
                    %endif
                </td>
                    <td>
                        ${invoice.officialNumber}
                    </td>
                    <td>
                        ${api.format_date(invoice.taskDate)}
                    </td>
                    <td>
                        <blockquote>
                            %if invoice.IDTask:
                                <a href="${request.route_path(route_name, id=invoice.IDTask)}"
                                title='Voir le document'>${invoice.number}</a>
                            %else:
                                ${invoice.number}
                            %endif
                            <small>${format_text(invoice.description)}
                        </blockquote>
                    </td>
                    <td class='invoice_company_name'>
                        ${format_client(invoice.get_client())}
                    </td>
                    <td>
                        <strong>${api.format_amount(invoice.total_ht())}&nbsp;€</strong>
                    </td>
                    <td>
                        ${api.format_amount(invoice.tva_amount())}&nbsp;€
                    </td>
                    <td>
                        % if len(task.payments) == 1 and task.is_resulted():
                            ${api.format_paymentmode(task.payments[0].mode)} le ${api.format_date(task.payments[0])}
                        % elif (len(task.payments) > 0:
                            <ul>
                                % for payment in task.payments:
                                    <li>
                                        ${api.format_amount(payment.amount)} ${api.format_paymentmode(payment.mode)} le ${api.format_date(payment.date)}
                                    </li>
                                % endfor
                            </ul>
                        % endif

                    </td>
                    <td>
                        %if invoice.IDTask:
                            <a class='btn'
                                href='${request.route_path(route_name, id=invoice.IDTask, _query=dict(view="pdf"))}'
                                title="Télécharger la version PDF">
                                <i class='icon icon-file'></i>
                           </a>
                        %endif
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='9'>
                    Aucune facture n'a pu être retrouvée
                </td>
            </tr>
        % endif
    </tbody>
    <tfoot>
        <tr>
            <td colspan='5'><strong>Total</strong></td>
            <td><strong>${api.format_amount(totalht)}&nbsp;€</strong></td>
            <td><strong>${api.format_amount(totaltva)}&nbsp;€</strong></td>
            <td colspan='3'></td>
        </tr>
    </tfoot>
</table>
${pager(invoices)}
</%block>
<%block name='footerjs'>
$('#client-select').chosen({allow_single_deselect: true});
$('#client-select').change(function(){$(this).closest('form').submit()});
$('#year-select').chosen({allow_single_deselect: true});
$('#year-select').change(function(){$(this).closest('form').submit()});
$('#paid-select').chosen({allow_single_deselect: true});
$('#paid-select').change(function(){$(this).closest('form').submit()});
</%block>
