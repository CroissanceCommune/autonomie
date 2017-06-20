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

<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='actionmenu'>
## We place the search form in the actionmenu since there are a few fields
    <% request.actionmenu.add(form) %>
    ${request.actionmenu.render(request)|n}
</%block>
<%block name='content'>
<%
## We build the link with the current search arguments
args = request.GET
url = request.route_path('customers.csv', id=request.context.id, _query=args)
%>
<a class='btn btn-default pull-right' href='${url}' title="Export au formt csv"><i class='fa fa-file'></i>CSV</a>

% if api.has_permission('add_customer'):
        <button class='btn btn-success' data-target="#customer-forms" aria-expanded="false" aria-controls="customer-forms" data-toggle='collapse'>
            <i class='glyphicon glyphicon-plus'></i>
            Ajouter un client
        </button>
        <a class='btn btn-default' href="${request.route_path('company_customers_import_step1', id=request.context.id)}">
            Importer des clients
        </a>

        <div class='collapse' id="customer-forms">
            <ul class="nav nav-tabs" role="tablist">
                <li role="presentation" class="active">
                    <a href="#companyForm" aria-controls="company" role="tab" data-toggle="tab">Client institutionnel</a>
                </li>
                <li role="presentation">
                    <a href="#individualForm" aria-controls="individual" role="tab" data-toggle="tab">Client particulier</a>
                </li>
            </ul>
            <div class="tab-content">

                <div role="tabpanel" class="tab-pane active row" id="companyForm">
                    <div class='col-xs-12 col-lg-6'>
                        <div class='container'>
                            <h2>${forms[0][0]}</h2>
                            ${forms[0][1].render()|n}
                        </div>
                    </div>
                </div>
                <div role="tabpanel" class="tab-pane row" id="individualForm">
                    <div class='col-xs-12'>
                        <div class='container'>
                            <h2>${forms[1][0]}</h2>
                            ${forms[1][1].render()|n}
                        </div>
                    </div>
                </div>
            </div>
    </div>
    <hr />
% endif
<table class="table table-striped table-condensed table-hover">
    <thead>
        <tr>
            <th class="visible-lg">${sortable("Code", "code")}</th>
            <th>${sortable("Entreprise", "name")}</th>
            <th class="visible-lg">${sortable("Nom du contact principal", "lastname")}</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for customer in records:
                <tr class='tableelement' id="${customer.id}">
                    <% url = request.route_path("customer", id=customer.id) %>
                    <% onclick = "document.location='{url}'".format(url=url) %>
                    <td onclick="${onclick}" class="visible-lg rowlink" >${customer.code}</td>
                    <td onclick="${onclick}" class="rowlink" >
                        % if customer.is_company():
                            ${customer.name}
                        % else:
                            Client particulier
                        % endif
                    </td>
                    <td onclick="${onclick}" class="visible-lg rowlink" >
                        % if customer.is_company():
                            ${customer.lastname} ${customer.firstname}
                        % else:
                            ${customer.get_name()}
                        % endif
                    </td>
                    <td class="actions">
                        % for btn in item_actions:
                            ${btn.render(request, customer)|n}
                        % endfor
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun client n'a été référencé pour l'instant
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(records)}
</%block>
