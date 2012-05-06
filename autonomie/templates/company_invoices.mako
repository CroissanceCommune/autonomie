<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="print_date" />
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_client" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="format_amount" />
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
            <select name='year' id='year-select' class='span2'>
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
            <div class='control-group'>
                <label class='control-label' for='search'>Identifiant du document</label>
                <div class='controls'>
                    <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}" />
            <button type="submit" class="btn btn-primary">Filtrer</button>
                </div>
            </div>
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
        <th>Statut</th>
        <th>Identifiant</th>
        <th>${sortable(u"Émise le", 'coop_task_taskDate')}</th>
        <th>${sortable(u"Nom", 'coop_task_number')}</th>
        <th>${sortable(u"Client", 'coop_customer_name')}</th>
        <th>Montant HT</th>
        <th>TVA</th>
        <th>Information de paiement</th>
        <th>PDF</th>
    </thead>
    <tbody>
        % if invoices:
            % for invoice in invoices:
                %if invoice.model.is_tolate():
                    <tr class='invoice_tolate_tr'>
                    <td class='invoice_tolate'>
                    %elif invoice.model.is_paid():
                        <tr class='invoice_paid_tr'>
                    <td class='invoice_paid'>
                            <span class="ui-icon ui-icon-check"></span>
                    %else:
                        <tr>
                    <td class='invoice_notpaid'>
                    %endif
                    <br />
                </td>
                    <td>
                        ${invoice.model.officialNumber}
                    </td>
                    <td>
                        ${print_date(invoice.model.taskDate)}
                    </td>
                    <td>
                        <blockquote>
                            %if invoice.model.project:
                                <a href="${request.route_path('invoice', cid=company.id, id=invoice.model.project.id, taskid=invoice.model.IDTask)}" title='Voir le document'>
                                ${invoice.model.number}<br />
                            </a>
                            %else:
                                ${invoice.model.number}
                            %endif
                            <small>${format_text(invoice.model.description)}
                        </blockquote>
                    </td>
                    <td class='invoice_company_name'>
                        ${format_client(invoice.get_client(), company)}
                    </td>
                    <td>
                        <strong>
                            ${format_amount(invoice.compute_totalht())} €
                        </strong>
                    </td>
                    <td>
                        ${format_amount(invoice.compute_tva())} €
                    </td>
                    <td>
                        %if invoice.model.is_paid():
                            ${invoice.model.get_paymentmode_str()} le ${print_date(invoice.model.statusDate)}
                        %endif
                    </td>
                    <td>
                        %if invoice.model.project:
                            <a class='btn'
                                href='${request.route_path("invoice", cid=company.id, id=invoice.model.IDProject, taskid=invoice.model.IDTask, _query=dict(view="pdf"))}'
                                title="Télécharger la version PDF">
                                <span class='ui-icon ui-icon-document'></span>
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
            <td><strong>${format_amount(sum([invoice.compute_totalht() for invoice in invoices]))} €</strong></td>
            <td><strong>${format_amount(sum([invoice.compute_tva() for invoice in invoices]))} €</strong></td>
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
