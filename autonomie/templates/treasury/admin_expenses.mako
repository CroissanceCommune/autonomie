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
<%doc>
Admin expenses list view
</%doc>
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='actionmenu'>
<div class='row-fluid'>
    <div class='span7'>
        <form class='form-search form-horizontal' id='search_form' method='GET'>
            <div style="padding-bottom:3px">
                <select name='year' id='year-select' class='span2'>
                    %for year_option in years:
                        %if unicode(year_option) == unicode(year):
                            <option selected="1" value='${year_option}'>${year_option}</option>
                        %else:
                            <option value='${year_option}'>${year_option}</option>
                        %endif
                    %endfor
                </select>
                <select name='month' id='month-select' class='span2' data-placeholder="Mois">
                    <option value='-1'></option>
                    %for id_, label in month_options:
                        <option
                        %if unicode(id_) == unicode(month):
                            selected="1"
                        %endif
                        value='${id_}'>${label}</option>
                    %endfor
                </select>
                <select id='owner-select' name='owner_id' data-placeholder="Nom de l'entrepreneur" class='span3'>
                    <option value='-1'></option>
                    %for id_, label in owner_options:
                            <option
                            %if id_ == unicode(owner_id):
                                    selected='1'
                                %endif
                                value='${id_}'>
                                    ${label}
                            </option>
                    %endfor
                </select>
                <select name='status' id='status-select' class='span2'>
                    %for label, value in status_options:
                        <option
                            %if value == status:
                                selected='1'
                            %endif
                            value='${value}'>
                                ${label}
                            </option>
                    %endfor
                </select>
                <select class='span2' name='items_per_page' id='items-select'>
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
                <td class='white_tr'><br /></td>
                <td>Notes de frais validées</td>
            </tr>
            <tr>
                <td class='green_tr'><br /></td>
                <td>Notes de fais payées</td>
            </tr>
            <tr>
                <td class='orange_tr'><br /></td>
                <td>Notes de frais en attente de validation</td>
            </tr>
        </table>
    </div>
</div>
</%block>
<%block name="content">
<table class="table table-condensed">
    <thead>
        <tr>
            <th>Identifiant</th>
            <th>Entrepreneur</th>
            <th>Période</th>
            <th>Montant</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % for expense in records:
            <% url = request.route_path('expense', id=expense.id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <%
if expense.status == 'valid':
    css = "white_"
elif expense.status == 'resulted':
    css = "green_"
else:
    css = "orange_"
%>
            <tr class="${css}tr">
                <td onclick="${onclick}" class="rowlink">
                    ${expense.id}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(expense.user)} ( ${expense.company.name} )
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.month_name(expense.month)} - ${expense.year}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_amount(expense.total, trim=True)|n}&nbsp;&euro;
                </td>
                <td>
                    <% url = request.route_path('expense', id=expense.id) %>
                    ${table_btn(url, u'Voir/Éditer', u"Voir la note de frais", icon="pencil" )}
                    <% url = request.route_path('expensexlsx', id=expense.id) %>
                    ${table_btn(url, u'Export', u"Télécharger au format Excel", icon="icon-file" )}
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
<%block name='footerjs'>
% for i in 'year', 'month', 'status', 'owner', 'items':
    $('#${i}-select').chosen({allow_single_deselect: true});
    $('#${i}-select').change(function(){$(this).closest('form').submit()});
% endfor
</%block>
