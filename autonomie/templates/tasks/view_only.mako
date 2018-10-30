<%doc>
 * Copyright (C) 2012-2017 Croissance Commune
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
    Base template for task readonly display
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name="headtitle">
${request.layout_manager.render_panel('task_title_panel', title=title)}
</%block>
<%block name='content'>
<div class='row'>
    <div class='col-xs-12 col-md-9'>
        <div class='panel panel-default page-block'>
            <div class='panel-heading'>
            % if hasattr(next, 'panel_heading'):
            ${next.panel_heading()}
            % endif
            </div>
            <div class='panel-body'>
                % if hasattr(next, 'before_task_tabs'):
                ${next.before_task_tabs()}
                % endif

                <div class="nav-tabs-responsive">
                    <ul class="nav nav-tabs" role="tablist">
                        <li role="presentation"
                            class="active"
                            >
                            <a href="#summary" aria-control="summary" role='tab' data-toggle='tab'>
                            Général
                            </a>
                        </li>
                        <li role="presentation"
                            >
                            <a href="#documents" aria-control="documents" role='tab' data-toggle='tab'>
                                Prévisualisation
                            </a>
                        </li>
                        % if hasattr(next, 'moretabs'):
                        ${next.moretabs()}
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
                    <div role='tabpanel' class="tab-pane active row" id="summary">
                        <div class='col-xs-12'>
                            % if hasattr(next, 'before_summary'):
                                ${next.before_summary()}
                            % endif
                            <hr />
                            % if indicators:
                            <h3>Indicateurs</h3>
                            ${request.layout_manager.render_panel('sale_file_requirements', file_requirements=indicators)}
                            % endif

                            <h3>Informations générales</h3>
                            <dl class='dl-horizontal'>
                                <dt>Statut</dt>
                                <dd>
                                <i class='glyphicon glyphicon-${api.status_icon(request.context)}'></i> ${api.format_status(request.context)}
                                </dd>
                                % if task.business_type and task.business_type.name != 'default':
                                % if task.business_id is not None:
                                    <dt>Affaire</dt>
                                    <dd><a href="${request.route_path('/businesses/{id}/overview', id=task.business_id)}">${task.business_type.label} : ${task.business.name}</a></dd>
                                % else:
                                    <dt>Affaire de type</dt>
                                    <dd>${task.business_type.label}</dd>
                                % endif
                                % endif
                                <dt>Nom du document</dt>
                                <dd>${request.context.name}</dd>
                                <dt>Date</dt>
                                <dd>${api.format_date(request.context.date)}</dd>
                                <dt>Client</dt>
                                <dd>
                                    ${request.context.customer.label}
                                    % if request.context.customer.code:
                                        (${request.context.customer.code})
                                    % endif
                                    <a href="${request.route_path('customer', id=request.context.customer.id)}">
                                        Voir le compte client
                                    </a>
                                </dd>
                                <dt>Montant HT</dt>
                                <dd>${api.format_amount(request.context.ht, precision=5)|n}&nbsp;€</dd>
                                <dt>TVA</dt>
                                <dd>${api.format_amount(request.context.tva, precision=5)|n}&nbsp;€ </dd>
                                <dt>TTC</dt>
                                <dd>${api.format_amount(request.context.ttc, precision=5)|n}&nbsp;€</dd>
                            </dl>
                            % if hasattr(next, 'after_summary'):
                                ${next.after_summary()}
                            % endif
                            <h3>Historique</h3>
                            % for status in request.context.statuses:
                            <blockquote>
                            ${status.status_comment | n}
                            <footer>
                            ${api.format_status_string(status.status_code)} - \
                            Par ${api.format_account(status.status_person)} le \
                            ${api.format_date(status.status_date)}</footer>
                            </blockquote>
                            % endfor
                        </div>
                    </div>


                    <div role="tabpanel" class="tab-pane row" id="documents">
                        <div class='col-xs-12'>
                            <div class="container-fluid task_view" style="border: 1px solid #dedede; background-color: #fdfdfd; margin:15px;">
                                ${request.layout_manager.render_panel('{0}_html'.format(task.type_), task=task)}
                            </div>
                        </div>
                    </div>

                    % if hasattr(next, 'moretabs_datas'):
                        ${next.moretabs_datas()}
                    % endif

                    <!-- attached files tab -->
                    % if api.has_permission('view.file'):
                        <% title = u"Liste des fichiers attachés à cette facture" %>
                       ${request.layout_manager.render_panel('task_file_tab', title=title)}
                    % endif

                </div>
            </div>
        </div>
    </div>
    <div class='col-xs-12 col-md-3'>
        <div class='panel panel-default page-block'>
            <div class='panel-body'>
                % if hasattr(next, 'before_actions'):
                ${next.before_actions()}
                % endif
                <a class='btn btn-primary primary-action btn-block'
                    href="${request.route_path('/%ss/{id}.pdf' % request.context.type_, id=request.context.id)}"
                    >
                    <i class='glyphicon glyphicon-book'></i>&nbsp;Voir le PDF
                </a>
                <hr />
                <div class='actions'>

                % if hasattr(next, 'moreactions'):
                ${next.moreactions()}
                % endif
                </div>
            </div>
        </div>
    </div>
</div>
</%block>
