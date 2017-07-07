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
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name='content'>
<div class='col-md-10 col-md-offset-1' style='overflow:hidden'>
    <div class='well'>
        <p>
            <span class="label label-important"><i class='glyphicon glyphicon-white icon-play'></i></span>
            %if task.status_person  is not UNDEFINED and task.status_person:
                <strong>${api.format_status(task)}</strong>
            %else:
                <strong>Aucune information d'historique ou de statut n'a pu être retrouvée.</strong>
            %endif
        </p>
        <ul>
        %if not api.has_permission('edit.%s' % task.type_):
            <li>
            <p>
                Vous ne pouvez plus modifier ce document. <br />
                ${api.format_main_status(task)}.
                % if hasattr(task, 'official_number') and task.official_number:
                    Il porte le numéro <b>${task.prefix}${task.official_number}</b>.
                % endif
            </p>
            </li>
        %elif task.status == 'wait':
            <li>
            <p>
                Vous ne pouvez plus modifier ce document car il est en attente de validation.
            </p>
            </li>
        % endif
        % if task.type_ == 'invoice':
            % if hasattr(task, 'estimation') and task.estimation:
                <li>
                <p>
                    Cette facture fait référence au devis : <a href="${request.route_path('/estimations/{id}.html', id=task.estimation.id)}">${task.estimation.internal_number}</a>
                </p>
                </li>
            % endif
            % if hasattr(task, 'cancelinvoices') and task.cancelinvoices:
                % for cancelinvoice in task.cancelinvoices:
                    <li>
                        <p>
                            L'avoir : \
                            <a href="${request.route_path('/cancelinvoices/{id}.html', id=cancelinvoice.id)}">
                                ${cancelinvoice.internal_number}
                            </a> a été généré depuis cette facture.
                        </p>
                    </li>
                % endfor
            % endif
            % if task.exported:
                <li>
                <p>
                    Cette facture a déjà été exportée
                </p>
                </li>
            % else:
                <li>
                <p>
                    Cette facture n'a pas encore été exportée
                </p>
                </li>
            % endif
        % elif task.type_ == 'estimation':
            % if hasattr(task, 'invoices') and task.invoices:
                <li>
                <p>
                    Les factures suivantes ont été générées depuis ce devis :
                    <ul class='list-unstyled'>
                        % for invoice in task.invoices:
                            <li>
                            <a href="${request.route_path('/invoices/{id}.html', id=invoice.id)}">${invoice.internal_number}</a>
                            </li>
                        % endfor
                    </ul>
                </p>
                </li>
            % endif
        % elif task.type_ == 'cancelinvoice':
            % if hasattr(task, 'invoice') and task.invoice:
                <li>
                <p>
                    Cet avoir est lié à la facture : <a href="${request.route_path('/invoices/{id}.html', id=task.invoice.id)}">
                        ${task.invoice.prefix}${task.invoice.official_number}
                    </a>
                </p>
                </li>
            % endif
        %endif
    </ul>

        % if hasattr(task, "status_comment") and task.status_comment:
            <b>Communication CAE-Entrepreneur</b>
            <p>
                ${task.status_comment}
            </p>
        % endif
        % if hasattr(task, "payments"):
            %if task.payments:
                Paiement reçu :
                <ul>
                % for payment in task.payments:
                    <% url = request.route_path('payment', id=payment.id) %>
                    <li>
                        <a href="${url}">
                            Remise "${payment.remittance_amount}"
                            le ${api.format_date(payment.date)} (${api.format_paymentmode(payment.mode)}
                            % if payment.bank:
                                ${payment.bank.label}
                            % endif
                            ):
                            ${api.format_amount(payment.amount, precision=5)|n}&nbsp;€
                            % if payment.tva is not None:
                                (${payment.tva.name})
                            % endif
                        </a>
                    </li>
                % endfor
                </ul>
            % endif
        % endif
        % if hasattr(task, 'topay') and not task.paid_status == 'resulted':
            Il reste ${api.format_amount(task.topay(), precision=5)|n}&nbsp;€ à régler.
        % endif
    </div>
            <% route = request.route_path('/%ss/{id}/status' % task.type_, id=task.id) %>
            <div class="well">
            <form id="deform" class="deform"
            accept-charset="utf-8"
            enctype="multipart/form-data"
            method="POST"
            action="${route}">
                % for button in submit_buttons:
                    <div style="padding:5px 5px; display:inline-block;">
                        ${button.render(request)|n}
                    </div>
                % endfor
        </form>
    </div>
        <div class='well'>
        <strong>Fichiers attachés à ce document</strong>
          ${format_filelist(task)}
          % if hasattr(task, 'estimation'):
            ${format_filelist(task.estimation)}
        % elif hasattr(task, 'invoice'):
            ${format_filelist(task.invoice)}
          % endif

    </div>
    <div class="container-fluid task_view" style="border: 1px solid #dedede; background-color: #fdfdfd;">
            ${request.layout_manager.render_panel('{0}_html'.format(task.type_), task=task)}
    </div>
</div>
</%block>
