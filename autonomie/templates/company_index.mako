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

<%doc>
    Company index page shows last events and elapsed invoices
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_customer" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='afteractionmenu'>
<% num_elapsed = elapsed_invoices.count() %>
<div class='page-header-block'>
    <h3>Bonjour ${api.format_account(request.user)}</h3>
    <div class='row'>
    % if num_elapsed:
        <div class='col-md-4 col-xs-12'>
        <small>
            <i class='glyphicon glyphicon-danger'></i>&nbsp;
            Vous avez des factures impayées depuis + de 45 jours
        </small>
        <ul class='list-group'>
            % for invoice in elapsed_invoices.limit(5):
            <li
                class='list-group-item clickable-row'
                data-href="${request.route_path("/invoices/{id}.html", id=invoice.id)}">
                <span class='label label-info'>${loop.index + 1}</span>&nbsp;
                ${format_customer(invoice.customer, False)} - ${api.format_amount(invoice.ttc, precision=5)}
            </li>
            % endfor
        </ul>
        <a class='' href="${request.route_path('company_invoices', id=company.id, _query=dict(__formid__='deform', status="notpaid"))}">
            Voir plus
        </a>
        </div>
    % endif
        <div class='col-md-8 col-xs-12'>
        % if request.config.has_key('welcome'):
            <p>
                ${format_text(request.config['welcome'])}
            </p>
        % endif
        </div>
    </div>
</div>
</%block>
<%block name='content'>
<div class='row'>
    <div class='col-md-6' id='tasklist_container'>
        ${panel('company_tasks')}
    </div>
    <div class='col-md-6' id='event_container'>
        ${panel('company_events')}
    </div>
</div>
</%block>
