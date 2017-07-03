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

<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    </li>
    <li>
    </li>
</ul>
<div>
    <form class='form-search ' id='search_form' method='GET'>
                <select name='year' id='year-select' class='col-md-2'>
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
                ${company.name} Solde de trésorerie au ${api.format_date(today)}
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
                    ${invoice.get_customer().name} - ${invoice.internal_number}
                </td>
                <td>
                    ${api.format_date(invoice.date)}
                </td>
                <td>
                    ${api.format_amount(invoice.total_ht(), precision=5)|n}
                </td>
            </tr>
        %endfor
    </tbody>
    <tfoot>
        <td colspan='2'>
            <strong>Solde de trésorerie</strong>
        </td>
        <td>
            <strong>${api.format_amount(sum([invoice.total_ht() for invoice in invoices]), precision=5)|n}&nbsp;€</strong>
        </td>
    </tfoot>
</table>
</%block>
<%block name='footerjs'>
$('#year-select').chosen({allow_single_deselect: true});
$('#year-select').change(function(){$(this).closest('form').submit()});
</%block>
