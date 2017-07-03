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
<%block name="headtitle">
${request.layout_manager.render_panel('task_title_panel', title=title)}
</%block>
<%block name='content'>
<div class='row'>
<div class='col-xs-12'>
<a class='btn btn-primary primary-action'
    href="${request.route_path(request.context.type_, id=request.context.id, _query={'view': 'pdf'})}"
    >
    <i class='glyphicon glyphicon-book'></i>&nbsp;Voir le PDF
</a>
<br />
<br />
</div>
</div>
<div class="nav-tabs-responsive">
    <ul class="nav nav-tabs" role="tablist">
        % if request.context.status == 'valid':
            <li role="presentation"
                class="active"
                >
                <a href="#summary" aria-control="summary" role='tab' data-toggle='tab'>
                Résumé
                </a>
            </li>
        % endif
        <li role="presentation"
            % if request.context.status != 'valid':
            class="active"
            % endif
            >
            <a href="#documents" aria-control="documents" role='tab' data-toggle='tab'>
                Prévisualisation
            </a>
        </li>
        <li role="presentation">
            <a href="#general_information" aria-control="general_information" role='tab' data-toggle='tab'>Informations générales</a>
        </li>
        % if api.has_permission('set_treasury.invoice'):
        <li role="presentation">
            <a href="#treasury" aria-control="treasury" role='tab' data-toggle='tab'>Informations comptables</a>
        </li>
        % endif
        % if api.has_permission('view.payment'):
        <li role="presentation">
            <a href="#payment" aria-control="payment" role='tab' data-toggle='tab'>Encaissements</a>
        </li>
        % endif
        % if api.has_permission('view.file'):
        <li role="presentation">
            <a href="#attached_files" aria-control="attached_files" role='tab' data-toggle='tab'>
                Fichiers attachés
                % if request.context.children:
                    <span class="badge">${len(request.context.children)}</span>
                % endif
            </a>
        </li>
        % endif
    </ul>
</div>
<div class='tab-content'>
    % if request.context.status == 'valid':
        <div role="tabpanel" class="tab-pane active row" id="summary">
        <h2>Résumé</h2>
        <h3>Contenu</h3>
            <dl class='dl-horizontal'>
            <dt>Date</dt>
            <dd>${api.format_date(request.context.date)}</dd>
            <dt>Client</dt>
            <dd>${request.context.customer.get_label()} <a href="${request.route_path('customer', id=request.context.customer.id)}">Voir le compte client</a></dd>
                <dt>Montant HT</dt>
                <dd>${api.format_amount(request.context.ht, precision=5)|n}&nbsp;€</dd>
                <dt>TVA</dt>
                <dd>${api.format_amount(request.context.tva, precision=5)|n}&nbsp;€ </dd>
                <dt>TTC</dt>
                <dd>${api.format_amount(request.context.ttc, precision=5)|n}&nbsp;€</dd>
            </dl>
        <h3>Historique</h3>
            % for payment in request.context.payments:
                % if loop.first:
                    <ul>
                % endif
                        <% url = request.route_path('payment', id=payment.id) %>
                        <li>
                        <a href="${url}">
                            Par ${api.format_account(payment.user)} :&nbsp;
                            ${api.format_amount(payment.amount)|n}&nbsp;€
                            le ${api.format_date(payment.date)}
                            (${api.format_paymentmode(payment.mode)})
                        </a>
                        </li>
                % if loop.last:
                    </ul>
                % endif

            % endfor
            ${api.format_status(request.context)}
        </div>
    % endif
    <div role="tabpanel" class="tab-pane
    % if request.context.status != 'valid':
    active
    % endif
    row" id="documents">
        <div class='col-md-12'>
            <div class="container-fluid task_view" style="border: 1px solid #dedede; background-color: #fdfdfd; margin:15px;">
                ${request.layout_manager.render_panel('{0}_html'.format(task.type_), task=task)}
            </div>
        </div>
    </div>

    <!-- General information tab -->
    <div role="tabpanel" class="tab-pane row" id="general_information">
        <div class="col-md-10 col-md-offset-1 col-xs-12">
        </div>
    </div>

    <!-- treasury tab -->
    % if api.has_permission('set_treasury.invoice'):
    <div role="tabpanel" class="tab-pane row" id="treasury">
        <div class="col-md-10 col-md-offset-1 col-xs-12">
        </div>
    </div>
    % endif
    % if api.has_permission('view.payment'):
    <div role="tabpanel" class="tab-pane row" id="payment">
        <div class="col-md-10 col-md-offset-1 col-xs-12">
        </div>
    </div>
    % endif

    <!-- attached files tab -->
    % if api.has_permission('view.file'):
        <% title = u"Liste des fichiers attachés à cette facture" %>
       ${request.layout_manager.render_panel('filelist_tab', title=title)}
    % endif

</div>

<div class='' id='forms_container'>
</div>
<div class='col-md-3' id='rightbar'>
</div>
</div>
</%block>
