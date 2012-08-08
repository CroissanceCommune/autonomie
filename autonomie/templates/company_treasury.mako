<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="print_date" />
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_amount" />
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    </li>
    <li>
    </li>
</ul>
<div>
    <form class='navbar-form form-search form-horizontal' id='search_form' method='GET'>
                <select name='year' id='year-select' class='span2'>
                    %for year in years:
                        %if unicode(current_year) == unicode(year):
                            <option selected="1" value='${year}'>${year}</option>
                        %else:
                            <option value='${year}'>${year}</option>
                        %endif
                    %endfor
                </select>
    </form>
</div>
</%block>
<%block name='content'>
<table class="table table-condensed table-bordered table-stripped">
    <thead>
        <tr>
            <th colspan='3'>
                ${company.name} Solde de trésorerie au ${print_date(today)}
            </th>
        </tr>
        <tr>
            <th>Nom de facture</th>
            <th>Date</th>
            <th>Montant</th>
        </tr>
    </thead>
    <tbody>
        %for invoice in invoices:
            <tr>
                <td>
                    ${invoice.get_client().name} - ${invoice.number}
                </td>
                <td>
                    ${print_date(invoice.taskDate)}
                </td>
                <td>
                    ${format_amount(invoice.total_ht())}
                </td>
            </tr>
        %endfor
    </tbody>
    <tfoot>
        <td colspan='2'>
            <strong>Solde de trésorerie</strong>
        </td>
        <td>
            <strong>${format_amount(sum([invoice.total_ht() for invoice in invoices]))}&nbsp;€</strong>
        </td>
    </tfoot>
</table>
</%block>
<%block name='footerjs'>
$('#year-select').chosen({allow_single_deselect: true});
$('#year-select').change(function(){$(this).closest('form').submit()});
</%block>
