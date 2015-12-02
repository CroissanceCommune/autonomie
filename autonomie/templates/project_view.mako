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
<%namespace file="base/utils.mako" import="print_date" />
<%namespace file="base/utils.mako" import="table_btn" />
<%namespace file="base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name='content'>
<div class="project-view">
<%def name="action_cell(task, view_url)">
    <% pdf_url = request.route_path(\
        task.type_,
        id=task.id, \
        _query=dict(view="pdf")) %>
    <% del_url = request.route_path(\
        task.type_,
        id=task.id,
        _query=dict(action="delete")) %>
    <td class="actions">
        ${table_btn(view_url, \
        u"Voir/Modifier", \
        u"Voir/éditer ce devis", \
        u"glyphicon glyphicon-pencil")}

        ${table_btn( \
        pdf_url,
        u"PDF", \
        u"Télécharger la version PDF", \
        u"glyphicon glyphicon-file")}
        %if task.is_deletable(request):
            ${table_btn(\
            del_url,\
            u"Supprimer", \
            u"Supprimer le document", \
            icon="glyphicon glyphicon-trash", \
            onclick=u"return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');",\
            css_class="btn-danger")}
        %endif
    </td>
</%def>

<%def name="estimation_row(task)">
<tr>
    <td>
        % if task.invoices:
            <div
                style="background-color:${task.color};\
                width:10px;">
                <br />
            </div>
        % endif
    </td>
    <% view_url = request.route_path(task.type_, id=task.id) %>

        <td
            class='rowlink'
            onclick="document.location='${view_url}'">
            ${task.name}
        </td>
        <td
            class='rowlink hidden-xs'
            onclick="document.location='${view_url}'">
        %if task.is_cancelled():
            <span class="label label-important">
                <i class="glyphicon glyphicon-white icon-remove"></i>
            </span>
        %elif task.is_draft():
            <i class='glyphicon glyphicon-bold'></i>
        %elif task.CAEStatus == 'geninv':
            <i class='glyphicon glyphicon-tasks'></i>
        %elif task.is_waiting():
            <i class='glyphicon glyphicon-time'></i>
        %endif
        ${api.format_status(task)}
    </td>
    ${action_cell(task, view_url)}
</tr>
</%def>
<%def name='invoice_row(task)'>
    <% view_url = request.route_path(task.type_, id=task.id) %>
<tr>
    <td>
        % if task.cancelinvoices or task.estimation:
            <div
                style="background-color:${task.color};\
                width:10px;">
                <br />
            </div>
        % endif
    </td>
    <td
        onclick="document.location='${view_url}'"
        class='rowlink'>
        ${request.config.get('invoiceprefix')}${task.official_number}
    </td>
    <td
        onclick="document.location='${view_url}'"
        class='rowlink'>
        ${task.name}
    </td>
    <td
        onclick="document.location='${view_url}'"
        class='rowlink hidden-xs'>
        %if task.is_cancelled():
            <span class="label label-important">
                <i class="glyphicon glyphicon-white icon-remove"></i>
            </span>
        %elif task.is_resulted():
            <i class='glyphicon glyphicon-ok'></i>
        %elif task.is_draft():
            <i class='glyphicon glyphicon-bold'></i>
        %elif task.is_waiting():
            <i class='glyphicon glyphicon-time'></i>
        %endif
        ${api.format_status(task)}
    </td>
    ${action_cell(task, view_url)}
</tr>
</%def>
<%def name='cancelinvoice_row(task)'>
    <% view_url = request.route_path(task.type_, id=task.id) %>
<tr>
    <td>
        <div
            style="background-color:${task.color};\
            width:10px;">
            <br />
        </div>
    </td>
    <td
        onclick="document.location='${view_url}'"
        class='rowlink'>
    ${request.config.get('invoiceprefix')}${task.official_number}
    % if task.invoice:
        (lié à la facture ${request.config.get('invoiceprefix')}${task.invoice.official_number})
    % endif
    </td>
    <td
        onclick="document.location='${view_url}'"
        class='rowlink'>
        ${task.name}
    </td>
    <td
        onclick="document.location='${view_url}'"
        class='rowlink hidden-xs'>
        %if task.is_valid():
            <i class='glyphicon glyphicon-ok'></i>
        %elif task.is_draft():
            <i class='glyphicon glyphicon-bold'></i>
        %endif
        ${api.format_status(task)}</td>
        ${action_cell(task, view_url)}
</tr>
</%def>
<br />
<div class='row collapse' id='project-description'>
    <div class="col-md-10 col-md-offset-1">
        <div class="well">
            <div class='row'>
                <div class='col-md-6'>
                    <h3>Client(s)</h3>
                    % for customer in project.customers:
                        <div class='well'>
                            <address>
                                ${format_text(customer.full_address)}
                            </address>
                        </div>
                    % endfor
                </div>
                <div class="col-md-6">
                    <dl>
                        %if project.type:
                            <dt>Type de projet :</dt> <dd>${project.type}</dd>
                        % endif
                        % if project.startingDate:
                            <dt>Début prévu le :</dt><dd>${api.format_date(project.startingDate)}</dd>
                        % endif
                        % if project.endingDate:
                            <dt>Livraison prévue le :</dt><dd>${api.format_date(project.endingDate)}</dd>
                        % endif
                    </dl>
                    <div class='well'>
                        <strong>Fichiers attachés à ce projet</strong>
                        ${format_filelist(project)}
                    </div>

                </div>
            </div>
            <h3>Définition du projet</h3>
            <p>
                ${format_text(project.definition)|n}
            </p>
            <br />
            <a class="btn btn-primary" title='Modifier les informations de ce client'
                href='${request.route_path("project", id=project.id, _query=dict(action="edit"))}'>
                Modifier
            </a>
        </div>
    </div>
</div>
<div class='row'>
    <div class='panel-group' id='phase_accordion'>
    %for phase in project.phases:
        % if len(project.phases) > 1:
            %if phase == latest_phase:
                <% section_css = 'in collapse' %>
            %else:
                <% section_css = 'collapse' %>
            %endif
            <div class='panel panel-default'>
                <div class='panel-heading section-header'>
                    <a href="#phase_${phase.id}"
                        data-toggle='collapse'
                        data-parent='#phase_accordion'
                        class='accordion-toggle'>
                            <%
if phase.is_default():
    label = u"Phase par défaut"
else:
    label = phase.name
%>
                            <i style="vertical-align:middle"
                                class="glyphicon glyphicon-folder-open">
                            </i>
                            &nbsp;${label}&nbsp;
                    </a>
                    <a
                        href="${request.route_path('phase', id=phase.id)}"
                        title="Éditer le libellé de cette phase"
                        >
                        <i style="vertical-align:middle"
                            class="glyphicon glyphicon-pencil">
                        </i>
                    </a>
                    % if len(phase.tasks) == 0:
                    <a
                        href="${request.route_path('phase', id=phase.id, _query=dict(action='delete'))}"
                        onclick="return confirm('Êtes-vous sûr de vouloir supprimer cette phase ?');"
                        title="Éditer le libellé de cette phase"
                        >
                        <i style="vertical-align:middle"
                            class="glyphicon glyphicon-trash">
                        </i>
                    </a>
                    % endif
                </div>
                <div class="panel-collapse ${section_css}"
                    id='phase_${phase.id}'>
                    <div class='panel-body'>
        % else:
            <div class='panel-group'>
                <div class='panel panel-default'>
                    <div class="panel-collapse" id='phase_${phase.id}'>
                        <div class='panel-body'>
        % endif

        <div class='header'>
            <h3 class='pull-left'>Devis</h3>
            <a
                class='btn btn-primary btn-small'
                href='${request.route_path("project_estimations", id=project.id, _query=dict(phase=phase.id))}'
                >
                <span class='fa fa-plus'></span>&nbsp;Nouveau devis
            </a>
        </div>
        % if  phase.estimations:
            <table class='table table-striped table-condensed'>
                <thead>
                    <th></th>
                    <th>Nom</th>
                    <th class="hidden-xs">État</th>
                    <th class="actions">Action</th>
                </thead>
                %for task in phase.estimations:
                    ${estimation_row(task)}
                %endfor
            </table>
        % else:
            <div class="alert alert-warning" style='clear:both'>Aucun devis n'a été créé</div>
        %endif
        <hr />
        <div class='header'>
            <h3 class='pull-left'>
                Facture(s), Avoir(s)
            </h3>
            <a class='btn btn-primary btn-small'
                href='${request.route_path(\
                "project_invoices", \
                id=project.id, \
                _query=dict(phase=phase.id))}'>
                <span class='fa fa-plus'></span>&nbsp;Nouvelle facture
            </a>
        </div>
        %if phase.invoices:
            <table class='table table-striped table-condensed'>
                <thead>
                    <th></th>
                    <th>Numéro</th>
                    <th>Nom</th>
                    <th class="hidden-xs">État</th>
                    <th style="text-align:center">Action</th>
                </thead>
                %for task in phase.invoices:
                    ${invoice_row(task)}
                %endfor
                % for task in phase.cancelinvoices:
                    ${cancelinvoice_row(task)}
                % endfor
            </table>
        % else:
            <div class="alert alert-warning" style='clear:both'>Aucune facture n'a été créée</div>
        % endif
        </div>
        </div>
        </div>
    %endfor
    </div>
    %if not project.phases:
        <strong>Aucune phase n'a été créée dans ce projet</strong>
    %endif
</div>
</div>
</%block>
<%block name="footerjs">
$( function() {
if (window.location.hash == "#showphase"){
$("#project-addphase").addClass('in');
}
});
</%block>
