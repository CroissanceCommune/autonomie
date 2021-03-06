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
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='afteractionmenu'>
<div class='page-header-block'>
<%
## We build the link with the current search arguments
args = request.GET
url = request.route_path('customers.csv', id=request.context.id, _query=args)
%>
<a
    class='btn btn-default pull-right'
    href='${url}'
    title="Export au formt csv"
    >
    <i class='fa fa-file'></i> CSV
</a>

% if api.has_permission('add_customer'):
    <button class='btn btn-primary primary-action' data-target="#customer-forms" aria-expanded="false" aria-controls="customer-forms" data-toggle='collapse'>
            <i class='glyphicon glyphicon-plus-sign'></i>
            Ajouter un client
        </button>
        <a class='btn btn-default' href="${request.route_path('company_customers_import_step1', id=request.context.id)}">
            <i class='fa fa-download'></i>
            Importer des clients
        </a>

        <div class='collapse' id="customer-forms">
            <h2>Ajouter un client</h2>
            <ul class="nav nav-tabs" role="tablist">
                <li role="presentation" class="active">
                <a href="#companyForm" aria-controls="company" role="tab" data-toggle="tab">Personne morale</a>
                </li>
                <li role="presentation">
                <a href="#individualForm" aria-controls="individual" role="tab" data-toggle="tab">Personne physique</a>
                </li>
            </ul>
            <div class="tab-content">

                <div role="tabpanel" class="tab-pane active row" id="companyForm">
                    <div class='col-md-12 col-lg-6'>
                        <div class='container'>
                            <h3>${forms[0][0]|n}</h3>
                            ${forms[0][1].render()|n}
                        </div>
                    </div>
                </div>
                <div role="tabpanel" class="tab-pane row" id="individualForm">
                    <div class='col-md-12 col-lg-6'>
                        <div class='container'>
                            <h3>${forms[1][0]|n}</h3>
                            ${forms[1][1].render()|n}
                        </div>
                    </div>
                </div>
            </div>
    </div>

% endif
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
<div class='panel-heading'>
<a  href='#filter-form' data-toggle='collapse' aria-expanded="false" aria-controls="filter-form">
    <i class='glyphicon glyphicon-search'></i>&nbsp;
    Filtres&nbsp;
    <i class='glyphicon glyphicon-chevron-down'></i>
</a>
% if '__formid__' in request.GET:
    <div class='help-text'>
        <small><i>Des filtres sont actifs</i></small>
    </div>
    <div class='help-text'>
        <a href="${request.current_route_path(_query={})}">
            <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
        </a>
    </div>
% endif
</div>
<div class='panel-body'>
    <div class='collapse' id='filter-form'>
        <div class='row'>
            <div class='col-xs-12'>
                ${form|n}
            </div>
        </div>
    </div>
</div>
</div>
<div class='panel panel-default page-block'>
<div class='panel-heading'>
${records.item_count} Résultat(s)
</div>
<div class='panel-body'>
<table class="table table-striped table-condensed table-hover">
    <thead>
        <tr>
            <th class="visible-lg">${sortable(u"Créé le", "created_at")}</th>
            <th class="visible-lg">${sortable(u"Code", "code")}</th>
            <th>${sortable(u"Nom du client", "label")}</th>
            <th class="visible-lg">${sortable(u"Nom du contact principal", "lastname")}</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for customer in records:
                <tr class='tableelement' id="${customer.id}">
                    <% url = request.route_path("customer", id=customer.id) %>
                    <% onclick = "document.location='{url}'".format(url=url) %>
                    <td onclick="${onclick}" class="visible-lg rowlink" >${api.format_date(customer.created_at)}</td>
                    <td onclick="${onclick}" class="visible-lg rowlink" >${customer.code}</td>
                    <td onclick="${onclick}" class="rowlink" >
                        % if customer.archived:
                            <span class='label label-warning'>Ce client a été archivé</span>
                        % endif
                        ${customer.label}
                    </td>
                    <td onclick="${onclick}" class="visible-lg rowlink" >
                        ${customer.get_name()}
                    </td>
                    <td class="actions">
                        ${request.layout_manager.render_panel('action_dropdown', links=stream_actions(customer))}
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun client n'a été référencé
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(records)}
</div></div>
</%block>
<%block name='footerjs'>
$(function(){
        $('input[name=search]').focus();
});
</%block>
