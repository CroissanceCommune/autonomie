<%doc>
    * Copyright (C) 2012-2016 Croissance Commune
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
<%inherit file="${context['main_template'].uri}" />
<%block name='mainblock'>
<% business = layout.current_business_object %>
<div class='row'>
    <div class='col-xs-12'>
        <div class='panel panel-default page-block'>
            <div class='panel-body'>
                % if business.closed:
                <div class='alert alert-success'>Cette affaire est clôturée</div>
                % else:
                <a
                    href="${invoice_all_url}"
                    % if not business.invoiced:
                    class='btn btn-primary'
                    % else:
                    class='btn btn-primary'
                    % endif
                    >
                    <i class='fa fa-plus-circle'></i>&nbsp;
                    % if business.invoiced:
                    Re-Générer toutes les factures
                    % else:
                    Générer toutes les factures
                    % endif
                </a>
                    <a
                        href="${estimation_add_url}"
                        class='btn btn-primary'
                        >
                        <i class='fa fa-plus-circle'></i>&nbsp;
                        Créer un devis
                    </a>
                % endif
                <h3>Devis de référence</h3>
                % if not estimations:
                    <em>Aucun devis n'est associé à cette affaire</em>
                % endif
                % for estimation in estimations:
                <div>
                    Devis :
                    <a
                        class="link"
                        href="${request.route_path('/estimations/{id}', id=estimation.id)}"
                        >
                        ${estimation.name} (${estimation.internal_number})
                    </a>
                </div>
                % endfor
                % if file_requirements or custom_indicators:
                <h3>Indicateurs</h3>
                % for indicator in custom_indicators:
                ${request.layout_manager.render_panel('custom_indicator', indicator=indicator)}
                % endfor
                ${request.layout_manager.render_panel('sale_file_requirements', file_requirements=file_requirements)}
                % endif
                % if payment_deadlines:
                <h3>Échéances de paiement</h3>
                    % for deadline in payment_deadlines:
                    <% url = request.route_path(invoice_deadline_route, id=business.id, deadline_id=deadline.id) %>
                    <hr />
                    <div class='row'>
                        % if deadline.deposit:
                        <div class='col-xs-6'>
                            <b>Facture d'acompte ${deadline.estimation.deposit} %</b>
                        </div>
                        % else:
                        <div class='col-xs-3'>
                            <b>${deadline.payment_line.description}</b>
                        </div>
                        <div class='col-xs-3'>
                            ${api.format_amount(deadline.payment_line.amount, precision=5) | n}&nbsp;€
                        </div>
                        % endif
                        % if deadline.invoice_id:
                        <div class='col-xs-3'>
                        <a href="${request.route_path('/invoices/{id}', id=deadline.invoice_id)}">
                        ${deadline.invoice.name} (${api.format_status(deadline.invoice)})
                        </a>
                        </div>
                            % if not business.closed:
                            <div class='col-xs-3'>
                                <a
                                    class='btn btn-default'
                                    href="${url}"
                                    >
                                    <i class='fa fa-copy'></i>&nbsp;
                                    Re-Générer la facture
                                </a>
                            </div>
                            % endif
                        % elif deadline.invoice_id:
                        <div class='col-xs-3'>
                        </div>
                            % if not business.closed:
                            <div class='col-xs-3'>
                                <a
                                    class='btn btn-default'
                                    href="${url}"
                                    >
                                    <i class='fa fa-copy'></i>&nbsp;
                                    Re-Générer la facture
                                </a>
                            </div>
                            % endif


                        % elif not deadline.deposit and deadline.payment_line.date:
                        <div class='col-xs-3'>
                            Facturation prévue le ${api.format_date(deadline.payment_line.date)}
                        </div>
                            % if not business.closed:
                            <div class='col-xs-3'>
                                <a class='btn btn-default'
                                    href="${url}">
                                <i class='fa fa-copy'></i>&nbsp;
                                Générer la facture</a>
                            </div>
                            % endif
                        % else:
                        <div class='col-xs-3'>
                            En attente de facturation
                        </div>
                            % if not business.closed:
                            <div class='col-xs-3'>
                                <a class='btn btn-default'
                                    href="${url}">
                                    <i class='fa fa-copy'></i>&nbsp;
                                Générer la facture</a>
                            </div>
                            % endif
                        % endif
                    </div>
                    % endfor
                % endif
            </div>
        </div>
    </div>
</div>
</%block>
