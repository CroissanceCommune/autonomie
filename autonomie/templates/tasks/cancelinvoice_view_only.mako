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
<% cancelinvoice = request.context %>
% if api.has_permission('draft.cancelinvoice'):
    <a class='btn btn-default btn-block' href="${request.route_path('/cancelinvoices/{id}/set_draft', id=cancelinvoice.id)}">
        <i class='glyphicon glyphicon-bold'></i> Repasser en brouillon
    </a>
% endif
<a class='btn btn-default btn-block'
    href="${request.route_path('/cancelinvoices/{id}/set_metadatas', id=cancelinvoice.id)}"
    >
    <i class='glyphicon glyphicon-pencil'></i> Modifier
</a>

% if api.has_permission('set_treasury.cancelinvoice'):
    <a class='btn btn-default btn-block' href="${request.route_path('/cancelinvoices/{id}/set_products', id=cancelinvoice.id)}">
        <i class='fa fa-cog'></i> Configurer les codes produits
    </a>
% endif
</%block>

<%block name='before_tabs'>
    <% cancelinvoice = request.context %>
    <h2>${cancelinvoice.name}</h2>
    <p class='lead'>
    Cet avoir porte le numéro <b>${cancelinvoice.official_number}</b>
    </p>
</%block>
<%block name='moretabs'>
    <% cancelinvoice = request.context %>
    <li role="presentation">
        <a href="#treasury" aria-control="treasury" role='tab' data-toggle='tab'>Comptabilité</a>
    </li>
</%block>
<%block name='before_summary'>
    <% cancelinvoice = request.context %>
<h3>Rattachement</h3>
<ul>
<li>
% if cancelinvoice.invoice:
    Cet avoir est rattaché à la facture \
    <a
    href="${request.route_path('/invoices/{id}.html', id=cancelinvoice.invoice.id)}"
    >
    ${cancelinvoice.invoice.internal_number}
    </a>
% else:
<div class='alert alert-danger'>
    <i class='glyphicon glyphicon-warning-sign'></i>
    Cet avoir n'est attaché à aucune facture (cela ne devrait pas se produire)
</div>
% endif
    </li>
        </ul>
</%block>

<%block name='moretabs_datas'>
    <% cancelinvoice = request.context %>
    <div role="tabpanel" class="tab-pane row" id="treasury">
        <div class='col-xs-12 col-md-10 col-md-offset-1'>
            <div class='alert'>
            Cet avoir est rattaché à l'année fiscale ${cancelinvoice.financial_year}.
            % if api.has_permission('set_treasury.cancelinvoice'):
            <a class='btn btn-primary btn-xs'
                href="${request.route_path('/cancelinvoices/{id}/set_treasury', id=cancelinvoice.id)}"
                >
                <i class='glyphicon glyphicon-pencil'></i> Modifier
            </a>
            % endif
            <br />
            Il porte le numéro ${cancelinvoice.official_number}.
            </div>
            <% url = request.route_path('/export/treasury/invoices/{id}', id=cancelinvoice.id, _query={'force': True}) %>
            % if cancelinvoice.exported:
                <div class='lead'>
                    <i class='glyphicon glyphicon-ok-sign'></i> Cet avoir a été exporté vers la comptabilité
                </div>
                    <a
                    href="${url}"
                    class='btn btn-default'
                    >
                    <i class='glyphicon glyphicon-export'></i>
                        Forcer la génération d'écritures pour cet avoir
                    </a>
            % else:
                <div class='lead'>
                    <i class='glyphicon glyphicon-time'></i> Cet avoir n'a pas encore été exporté vers la comptabilité
                </div>
                % if api.has_permission('admin_treasury'):
                    <a
                    href="${url}"
                    class='btn btn-primary primary-action'
                    >
                    <i class='glyphicon glyphicon-export'></i>
                        Générer les écritures pour cet avoir
                    </a>
                % endif
            % endif
            </div>
        </div>
</%block>
