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
        ${task.prefix}${task.official_number}
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
    ${task.prefix}${task.official_number}
    % if task.invoice:
        (lié à la facture ${task.invoice.prefix}${task.invoice.official_number})
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

<div class="nav-tabs-responsive">
    <ul class="nav nav-tabs" role="tablist">
        <li role="presentation" class="active">
            <a href="#documents" aria-control="documents" role='tab' data-toggle='tab'>
                Documents
            </a>
        </li>
        <li role="presentation">
            <a href="#general_information" aria-control="general_information" role='tab' data-toggle='tab'>Informations générales</a>
        </li>
        <li role="presentation">
            <a href="#attached_files" aria-control="attached_files" role='tab' data-toggle='tab'>
                Fichiers attachés
                % if project.children:
                    <span class="badge">${len(project.children)}</span>
                % endif
            </a>
        </li>
    </ul>
</div>
<div class='tab-content'>
    <!-- Documents tab -->
    <div role="tabpanel" class="tab-pane active row" id="documents">
        <button class='btn btn-default large-btn'
            data-target="#phase-form"
            aria-expanded="false"
            aria-controls="phase-form"
            data-toggle='collapse'>
            <i class='glyphicon glyphicon-plus'></i>
            Ajouter un dossier
        </button>

        <div class='collapse' id='phase-form'>
            <h3>Ajouter un dossier</h3>
            ${phase_form.render()|n}
        </div>
        <hr />


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
                                        label = u"Dossier par défaut"
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
                                title="Éditer le libellé de ce dossier"
                                >
                                <i style="vertical-align:middle"
                                    class="glyphicon glyphicon-pencil">
                                </i>
                            </a>
                            % if len(phase.tasks) == 0:
                                <a
                                    href="${request.route_path('phase', id=phase.id, _query=dict(action='delete'))}"
                                    onclick="return confirm('Êtes-vous sûr de vouloir supprimer cet élément ?');"
                                    title="Supprimer ce dossier"
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
                    <div class='panel panel-default'>
                        <div class="panel-collapse" id='phase_${phase.id}'>
                            <div class='panel-body'>
            % endif

        <div class='header'>
            <h3 class='pull-left'>Devis</h3>
            <a
                class='btn btn-success large-btn'
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
            <a class='btn btn-success large-btn'
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

    <!-- General information tab -->
    <div role="tabpanel" class="tab-pane row" id="general_information">
        <div class="col-md-10 col-md-offset-1 col-xs-12">
            <a class='btn btn-primary large-btn'
                href="${request.route_path('project', id=request.context.id, _query={'action': 'edit'})}"
                title="Modifier le projet">
                <i class='glyphicon glyphicon-pencil'></i>
                Modifier
            </a>
            <h3>Client(s)</h3>
            % for customer in project.customers:
                <div class=''>
                    <a href="${request.route_path('customer', id=customer.id, _query={'action': 'edit'})}"
                        class='btn btn-default btn-small pull-right'
                        title="Modifier ce client">
                        <i class='glyphicon glyphicon-pencil'></i> Modifier
                    </a>
                    <address>
                        ${format_text(customer.full_address)}
                    </address>
                    <div class='clearfix'></div>
                    <hr />
                </div>
            % endfor
            <h3>Informations générales</h3>
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
            % if project.definition:
                <h3>Définition du projet</h3>
                <p>
                    ${format_text(project.definition)|n}
                </p>
            % endif
        </div>
    </div>

    <!-- attached files tab -->
    <div role="tabpanel" class="tab-pane row" id="attached_files">
        <div class="col-md-10 col-md-offset-1 col-xs-12">
            <a class='btn btn-primary large-btn'
                href="${request.route_path('project', id=project.id, _query={'action': 'attach_file'})}"
                title="Attacher un fichier">
                <i class='glyphicon glyphicon-plus-sign'></i>
               Attacher un fichier
            </a>
            <h3>Liste des fichiers rattachés à ce projet</h3>
            % for child in project.children:
                % if child.type_ == 'file':
                    <div>
                        <dl class='dl-horizontal'>
                            <dt>Description du fichier</dt><dd>${child.description}</dd>
                            <dt>Taille du fichier</dt><dd>${api.human_readable_filesize(child.size)}</dd>
                            <dt>Dernière modification</dt><dd>${api.format_date(child.updated_at)}</dd>
                        </dl>
                          % if api.has_permission('edit_file', child):
                              <a class='btn btn-default btn-small'
                                  href="${request.route_path('file', id=child.id)}">
                                  <i class='glyphicon glyphicon-pencil'></i> Voir/modifier
                              </a>
                          % endif
                              <a class='btn btn-default btn-small'
                                  href="${request.route_path('file', id=child.id, _query=dict(action='download'))}">
                                  <i class='glyphicon glyphicon-download'></i> Télécharger
                              </a>
                          % if api.has_permission('edit_file', child):
                              <a class='btn btn-small btn-danger'
                                    href="${request.route_path('file', id=child.id, _query=dict(action='delete'))}"
                                    onclick="return confirm('Supprimer ce fichier ?');">
                                  <i class='glyphicon glyphicon-trash'></i> Supprimer
                              </a>
                         % endif
                    </div>
                    <hr />
                % endif
            % endfor
        </div>
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
