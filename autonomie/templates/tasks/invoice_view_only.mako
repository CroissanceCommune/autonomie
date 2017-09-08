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
<% invoice = request.context %>
% if api.has_permission('add_payment.invoice'):
    <a class='btn btn-default primary-action btn-block' href="${request.route_path('/invoices/{id}/addpayment', id=invoice.id)}">
        <i class='fa fa-bank'></i> Enregistrer un encaissement
    </a>
% endif
% if api.has_permission('gencinv.invoice'):
    <a class='btn btn-default btn-block' href="${request.route_path('/invoices/{id}/gencinv', id=invoice.id)}">
        <i class='fa fa-files-o'></i> Générer un avoir
    </a>
% endif
% if api.has_permission('draft.invoice'):
    <a class='btn btn-default btn-block' href="${request.route_path('/invoices/{id}/set_draft', id=invoice.id)}">
        <i class='glyphicon glyphicon-bold'></i> Repasser en brouillon
    </a>
% endif
<a class='btn btn-default btn-block'
    href="${request.route_path('/invoices/{id}/set_metadatas', id=invoice.id)}"
    >
    <i class='glyphicon glyphicon-pencil'></i> Modifier
</a>
% if api.has_permission('duplicate.invoice'):
<a class='btn btn-default btn-block' href="${request.route_path('/invoices/{id}/duplicate', id=invoice.id)}">
    <i class='fa fa-copy'></i> Dupliquer
</a>
% endif

% if api.has_permission('set_treasury.invoice'):
    <a class='btn btn-default btn-block' href="${request.route_path('/invoices/{id}/set_products', id=invoice.id)}">
        <i class='fa fa-cog'></i> Configurer les codes produits
    </a>
% endif

</%block>

<%block name='before_tabs'>
    <% invoice = request.context %>
    <h2>${invoice.name}</h2>
    <p class='lead'>
    Cette facture porte le numéro <b>${invoice.prefix}${invoice.official_number}</b>
    </p>
</%block>
<%block name='moretabs'>
    <% invoice = request.context %>
    <li role="presentation">
        <a href="#treasury" aria-control="treasury" role='tab' data-toggle='tab'>Comptabilité</a>
    </li>

    <li role="presentation">
        <a href="#payment" aria-control="payment" role='tab' data-toggle='tab'>Encaissements</a>
    </li>
</%block>
<%block name='before_summary'>
    <% invoice = request.context %>
<h3>Rattachement</h3>
<ul>
<li>
% if invoice.estimation:
    Cette facture est rattachée au devis \
    <a
    href="${request.route_path('/estimations/{id}.html', id=invoice.estimation.id)}"
    >
    ${invoice.estimation.internal_number}
    </a>
    <a
        href="${request.route_path('/invoices/{id}/attach_estimation', id=invoice.id)}"
        class='btn btn-primary btn-xs'>
        <i class='glyphicon glyphicon-link'></i> Modifier
    </a>
% else:
<div>Aucun devis n'est rattaché à cette facture
    <a
        href="${request.route_path('/invoices/{id}/attach_estimation', id=invoice.id)}"
        class='btn btn-primary btn-xs'>
        <i class='glyphicon glyphicon-link'></i> Rattacher cette facture à un devis
    </a>
</div>
% endif
    </li>
<br />
% if invoice.cancelinvoices:
    % for  cancelinvoice in invoice.cancelinvoices:
            <li>
                <p>
                    L'avoir (${api.format_cancelinvoice_status(cancelinvoice, full=False)}): \
                    <a href="${request.route_path('/cancelinvoices/{id}.html', id=cancelinvoice.id)}">
                        ${cancelinvoice.internal_number}
                        % if cancelinvoice.official_number:
                        (${cancelinvoice.prefix}${cancelinvoice.official_number})
                        % endif
                    </a> a été généré depuis cette facture.
                </p>
            </li>
    % endfor
% else:
<li>
    Aucun avoir n'a été généré
    </li>
% endif
        </ul>
</%block>

<%block name='moretabs_datas'>
    <% invoice = request.context %>
    <div role="tabpanel" class="tab-pane row" id="treasury">
        <div class='col-xs-12'>
        <div class='alert'>
        Cette facture est rattachée à l'année fiscale ${invoice.financial_year}.
        % if api.has_permission('set_treasury.invoice'):
        <a class='btn btn-primary btn-xs'
            href="${request.route_path('/invoices/{id}/set_treasury', id=invoice.id)}"
            >
            <i class='glyphicon glyphicon-pencil'></i> Modifier
        </a>
        % endif
        <br />
        Elle porte le numéro ${invoice.prefix}${invoice.official_number}.
        </div>
        <% url = request.route_path('/export/treasury/invoices/{id}', id=invoice.id, _query={'force': True}) %>
            % if invoice.exported:
                <div class='lead'>
                    <i class='glyphicon glyphicon-ok-sign'></i> Cette facture a été exportée vers la comptabilité
                </div>
                % if api.has_permission('admin_treasury'):
                    <a
                    href="${url}"
                    class='btn btn-default'
                    >
                    <i class='glyphicon glyphicon-export'></i>
                        Forcer la génération d'écritures pour cette facture
                    </a>
                % endif
            % else:
                <div class='lead'>
                    <i class='glyphicon glyphicon-time'></i> Cette facture n'a pas encore été exportée vers la comptabilité
                </div>
                % if api.has_permission('admin_treasury'):
                    <a
                    href="${url}"
                    class='btn btn-primary primary-action'
                    >
                    <i class='glyphicon glyphicon-export'></i>
                        Générer les écritures pour cette facture
                    </a>
                % endif
            % endif
        </div>
    </div>
    <div role="tabpanel" class="tab-pane row" id="payment">
        <div class="col-xs-12">
        % if api.has_permission('add_payment.invoice'):
            <a
                href="${request.route_path('/invoices/{id}/addpayment', id=invoice.id)}"
                class='btn btn-primary primary-action'
                >
            <i class='glyphicon glyphicon-plus-sign'></i> Enregistrer un encaissement
            </a>
        % endif
        <h3>Liste des encaissements</h3>
        % if invoice.payments:
            % for payment in invoice.payments:
                    % if loop.first:
                        <ul>
                    % endif
                        <% url = request.route_path('payment', id=payment.id) %>
                        <li>
                        <a href="${url}">
                            Enregistré par ${api.format_account(payment.user)} :&nbsp;
                            ${api.format_amount(payment.amount, precision=5)|n}&nbsp;€
                            le ${api.format_date(payment.date)}
                            (${api.format_paymentmode(payment.mode)})
                        </a>
                        </li>
                    % if loop.last:
                        </ul>
                    % endif
            % endfor
        % else:
            Aucun encaissement n'a été saisi
        % endif
        <h3>Avoir(s)</h3>
        % if invoice.cancelinvoices:
            <% hasone = False %>
            <ul>
            % for  cancelinvoice in invoice.cancelinvoices:
                % if cancelinvoice.status == 'valid':
                    <% hasone = True %>
                    <li>
                        <p>
                            L'avoir : \
                            <a href="${request.route_path('/cancelinvoices/{id}.html', id=cancelinvoice.id)}">
                                ${cancelinvoice.internal_number}
                                (numéro ${cancelinvoice.prefix}${cancelinvoice.official_number})
                                d'un montant TTC de ${api.format_amount(cancelinvoice.ttc, precision=5)|n} €
                            </a> a été généré depuis cette facture.
                        </p>
                    </li>
                 % endif
            % endfor
            </ul>
            % if not hasone:
                Aucun avoir validé n'est associé à ce document
            % endif
        % else:
        Aucun avoir validé n'est associé à ce document
        % endif
        </div>
    </div>
</%block>
