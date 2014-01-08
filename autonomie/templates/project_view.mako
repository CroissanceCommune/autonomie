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
<div class='row-fluid collapse' id='project-addphase'>
    <div class='span4 offset4'>
        <h3>Ajouter une phase</h3>
        <form class='navbar-form' method='POST' action="${request.route_path('project', id=project.id, _query=dict(action='addphase'))}">
            <input type='text' name='phase' />
            <button class='btn btn-primary' type='submit' name='submit' value='addphase'>Valider</button>
        </form>
        <br />
    </div>
</div>
<div class='row-fluid collapse' id='project-description'>
    <div class="span8 offset2">
        <div class="well">
            <div class='row-fluid'>
                <div class='span6'>
                    <h3>Client(s)</h3>
                    % for customer in project.customers:
                        <div class='well'>
                            <address>
                                ${format_text(customer.full_address)}
                            </address>
                        </div>
                    % endfor
                </div>
                <div class="span6">
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
            <a class="btn btn-primary" title='Éditer les informations de ce client'
                href='${request.route_path("project", id=project.id, _query=dict(action="edit"))}'>
                Éditer
            </a>
        </div>
    </div>
</div>
<div class='row-fluid'>
    %if len(project.phases)>1:
        <% section_css = 'collapse' %>
    %else:
        <% section_css = 'in collapse' %>
    %endif
    %for phase in project.phases:
        % if not phase.is_default():
            <div class='section-header'>
                <a href="#" data-toggle='collapse' data-target='#phase_${phase.id}'>
                    <div>
                        <i style="vertical-align:middle" class="icon-folder-open"></i>&nbsp;${phase.name}
                    </div>
                </a>
            </div>
             <div class="section-content ${section_css}" id='phase_${phase.id}'>
        % else:
             <div class="section-content" id='phase_${phase.id}'>
        % endif
        <h3 class='pull-left' style="padding-right:10px;">Devis</h3>
        <a class='btn' href='${request.route_path("project_estimations", id=project.id, _query=dict(phase=phase.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>Nouveau devis
        </a>
        % if  phase.estimations:
            <table class='table table-striped table-condensed'>
                <thead>
                    <th></th>
                    <th>Document</th>
                    <th class="hidden-phone">Nom</th>
                    <th class="hidden-phone">État</th>
                    <th style="text-align:center">Action</th>
                </thead>
                %for task in phase.estimations:
                    <tr>
                        <td>
                            % if task.invoices:
                                <div style="background-color:${task.color};width:10px;">
                                    <br />
                                </div>
                            % endif
                        </td>
                        <% task.url = request.route_path("estimation", id=task.id) %>
                        <td class='rowlink' onclick="document.location='${task.url}'">${task.number}</td>
                        <td class='rowlink hidden-phone' onclick="document.location='${task.url}'">${task.name}</td>
                        <td class='rowlink hidden-phone' onclick="document.location='${task.url}'">
                            %if task.is_cancelled():
                                <span class="label label-important">
                                    <i class="icon-white icon-remove"></i>
                                </span>
                            %elif task.is_draft():
                                <i class='icon icon-bold'></i>
                            %elif task.CAEStatus == 'geninv':
                                <i class='icon icon-tasks'></i>
                            %elif task.is_waiting():
                                <i class='icon icon-time'></i>
                            %endif
                            ${api.format_status(task)}
                        </td>
                        <td style="text-align:right">
                            ${table_btn(task.url, u"Voir/Éditer", u"Voir/éditer ce devis", u"icon-pencil")}
                            ${table_btn(request.route_path("estimation", id=task.id, _query=dict(view="pdf")), u"PDF", u"Télécharger la version PDF", u"icon-file")}
                            %if task.is_deletable(request):
                                ${table_btn(request.route_path("estimation", id=task.id, _query=dict(action="delete")), u"Supprimer", u"Supprimer le devis", icon="icon-trash", onclick=u"return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');")}
                            %endif
                        </td>
                    </tr>
                %endfor
            </table>
        % else:
            <div style='clear:both'>Aucun devis n'a été créé
            % if not phase.is_default():
                dans cette phase
            % endif
            </div>
        %endif
        <h3 class='pull-left' style='padding-right:10px;font-weight:100;'>Facture(s)</h3>
        <a class='btn' href='${request.route_path("project_invoices", id=project.id, _query=dict(phase=phase.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>Nouvelle facture
        </a>
        %if phase.invoices:
            <table class='table table-striped table-condensed'>
                <thead>
                    <th></th>
                    <th>Numéro</th>
                    <th>Document</th>
                    <th class="hidden-phone">Nom</th>
                    <th class="hidden-phone">État</th>
                    <th style="text-align:center">Action</th>
                </thead>
                %for task in phase.invoices:
                    <tr>
                        <td>
                            % if task.cancelinvoice or task.estimation:
                                <div style="background-color:${task.color};width:10px;">
                                    <br />
                                </div>
                            % endif
                        </td>
                        <% task.url = request.route_path("invoice", id=task.id) %>
                        <td onclick="document.location='${task.url}'" class='rowlink'>
                            ${request.config.get('invoiceprefix')}${task.officialNumber}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>${task.number}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink hidden-phone'>${task.name}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink hidden-phone'>
                            %if task.is_cancelled():
                                <span class="label label-important">
                                    <i class="icon-white icon-remove"></i>
                                </span>
                            %elif task.is_resulted():
                                <i class='icon icon-ok'></i>
                            %elif task.is_draft():
                                <i class='icon icon-bold'></i>
                            %elif task.is_waiting():
                                <i class='icon icon-time'></i>
                            %endif
                            ${api.format_status(task)}
                        </td>
                        <td style="text-align:right">
                            ${table_btn(task.url, u"Voir/Éditer", u"Voir/éditer cette facture", u"icon-pencil")}
                            ${table_btn(request.route_path("invoice", id=task.id, _query=dict(view="pdf")), u"PDF", u"Télécharger la version PDF", u"icon-file")}
                            %if task.is_deletable(request):
                                ${table_btn(request.route_path("invoice", id=task.id, _query=dict(action="delete")), u"Supprimer", u"Supprimer le devis", icon="icon-trash", onclick=u"return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');")}
                            %endif
                        </td>
                    </tr>
                %endfor
                % for task in phase.cancelinvoices:
                    <tr>
                        <td>
                            <div style="background-color:${task.color};width:10px;">
                                <br />
                            </div>
                        </td>
                        <% task.url = request.route_path("cancelinvoice", id=task.id) %>
                        <td onclick="document.location='${task.url}'" class='rowlink'>
                            ${request.config.get('invoiceprefix')}${task.officialNumber}
                            % if task.invoice:
                                (lié à la facture ${request.config.get('invoiceprefix')}${task.invoice.officialNumber})
                            % endif
                        </td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>${task.number}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>${task.name}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>
                            %if task.is_valid():
                                <i class='icon icon-ok'></i>
                            %elif task.is_draft():
                                <i class='icon icon-bold'></i>
                            %endif
                            ${api.format_status(task)}</td>
                        <td style="text-align:right">
                            ${table_btn(task.url, u"Voir/Éditer", u"Voir/éditer cet avoir", u"icon-pencil")}
                            ${table_btn(request.route_path("cancelinvoice", id=task.id, _query=dict(view="pdf")), u"PDF", u"Télécharger la version PDF", u"icon-file")}
                        </td>
                    </tr>
                % endfor
            </table>
        % else:
            <div style='clear:both'>Aucune facture n'a été créée
                %if not phase.is_default():
                    dans cette phase
                %endif
            </div>
        % endif
        </div>
    %endfor
    %if not project.phases:
        <strong>Aucune phase n'a été créée dans ce projet</strong>
    %endif
</div>
</%block>
<%block name="footerjs">
$( function() {
if (window.location.hash == "#showphase"){
$("#project-addphase").addClass('in');
}
});
</%block>
