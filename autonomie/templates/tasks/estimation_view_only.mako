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
    Base template for task readonly display
</%doc>
<%inherit file="/tasks/view_only.mako" />
<%namespace file="/base/utils.mako" import="format_filelist" />

<%block name='moreactions'>
<% estimation = request.context %>
% if api.has_permission('geninv.estimation'):
    <a class='btn btn-default btn-block' href="${request.route_path('/estimations/{id}/geninv', id=estimation.id)}">
        <i class='fa fa-files-o'></i>&nbsp;
        % if len(estimation.invoices) or estimation.geninv:
            Re-générer des factures
        % else:
            Générer des factures
        % endif
    </a>
% elif api.has_permission('genbusiness.estimation'):
    % if estimation.business_id:
    <a
        class='btn btn-default btn-block'
        href="${request.route_path('/businesses/{id}', id=estimation.business_id)}"
        title="Voir l'affaire"
        >
        <i class='fa fa-files-o'></i>&nbsp;Voir l'affaire ${estimation.business.name}
        </a>
    % else:
    <a
        class='btn btn-default btn-block'
        href="${request.route_path('/estimations/{id}/genbusiness', id=estimation.id)}"
        title="Générer une affaire au sein de laquelle facturer"
        >
        <i class='fa fa-files-o'></i>&nbsp;
        Générer une affaire (${estimation.business_type.label})
    </a>
    % endif
% endif
% if api.has_permission('duplicate.estimation'):
<a class='btn btn-default btn-block' href="${request.route_path('/estimations/{id}/duplicate', id=estimation.id)}">
    <i class='fa fa-copy'></i> Dupliquer
</a>
% endif
% if api.has_permission('draft.estimation'):
    <a class='btn btn-default btn-block' href="${request.route_path('/estimations/{id}/set_draft', id=estimation.id)}">
        <i class='glyphicon glyphicon-bold'></i> Repasser en brouillon
    </a>
% endif
<a class='btn btn-default btn-block'
    href="${request.route_path('/estimations/{id}/set_metadatas', id=estimation.id)}"
    >
    <i class='glyphicon glyphicon-pencil'></i> Modifier
</a>
% if not estimation.invoices:
    <a
        href="${request.route_path('/estimations/{id}/attach_invoices', id=estimation.id)}"
        class='btn btn-primary btn-xs'>
        <i class='glyphicon glyphicon-link'></i> Rattacher ce devis à des factures
    </a>
% endif
</%block>

<%block name='before_actions'>
    <% estimation = request.context %>
    <h2>
    ${estimation.name}
    </h2>
</%block>
<%block name='before_summary'>
<br />
<br />
    <% estimation = request.context %>
% if api.has_permission('set_signed_status.estimation'):
    <div
        class="btn-group signed_status_group"
        data-toggle="buttons"
        data-url="${request.route_path('/api/v1/estimations/{id}', id=estimation.id, _query={'action': 'signed_status'})}"
        >
        % for action  in actions:
            <label class="${action.options['css']}
            % if estimation.signed_status == action.name:
            active
            % endif
            ">
            <input
                type="radio"
                title="${action.options['title']}"
                name="${action.status_attr}"
                value="${action.name}"
                autocomplete="off"
                % if estimation.signed_status == action.name:
                checked
                % endif
                > <i class='glyphicon glyphicon-${action.options['icon']}'></i> ${action.options['label']}
            </label>
        % endfor
    </div>
% endif
% if estimation.invoices:
<div>
<h3 class='inline-element'>Factures</h3>
    <a
        href="${request.route_path('/estimations/{id}/attach_invoices', id=estimation.id)}"
        >
        <i class='fa fa-pencil'></i>
    </a>
<ul>
    % for invoice in estimation.invoices:
            <li>
                <p>
                    La facture (${api.format_invoice_status(invoice, full=False)}): \
                    <a href="${request.route_path('/invoices/{id}.html', id=invoice.id)}">
                        ${invoice.internal_number}
                        % if invoice.official_number:
                        (${invoice.official_number})
                        % endif
                    </a> a été générée depuis ce devis.
                </p>
            </li>
    % endfor
    </ul>
</div>
% endif
</%block>
