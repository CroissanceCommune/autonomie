<%inherit file="base.mako"></%inherit>
<%namespace file="base/utils.mako" import="print_date" />
<%namespace file="base/utils.mako" import="table_btn" />
<%namespace file="base/utils.mako" import="format_text" />
<%block name='content'>
<div class='row collapse' id='project-addphase'>
    <div class='span4 offset4'>
        <h3>Ajouter une phase</h3>
        <form class='navbar-form' method='POST' action="${request.route_path('project', id=project.id, _query=dict(action='addphase'))}">
            <input type='text' name='phase' />
            <button class='btn btn-primary' type='submit' name='submit' value='addphase'>Valider</button>
        </form>
        <br />
    </div>
</div>
<div class='row collapse' id='project-description'>
    <div class="span8 offset2">
        <div class="well">
            <div class='row'>
                <div class='span3'>
                    <h3>Client(s)</h3>
                    % for client in project.clients:
                        <div class='well'>
                            <address>
                                ${format_text(client.full_address)}
                            </address>
                        </div>
                    % endfor
                </div>
                <div class="span3">
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
<div class='container'>
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
        <h3 class='floatted' style="padding-right:10px;">Devis</h3>
        <a class='btn' href='${request.route_path("project_estimations", id=project.id, _query=dict(phase=phase.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>
        </a>
        % if  phase.estimations:
            <table class='table table-striped table-condensed'>
                <thead>
                    <th></th>
                    <th>Document</th>
                    <th>Nom</th>
                    <th>État</th>
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
                        <td class='rowlink' onclick="document.location='${task.url}'">${task.name}</td>
                        <td class='rowlink' onclick="document.location='${task.url}'">
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
        <h3 class='floatted' style='padding-right:10px;font-weight:100;'>Facture(s)</h3>
        <a class='btn' href='${request.route_path("project_invoices", id=project.id, _query=dict(phase=phase.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>
        </a>
        %if phase.invoices:
            <table class='table table-striped table-condensed'>
                <thead>
                    <th></th>
                    <th>Numéro</th>
                    <th>Document</th>
                    <th>Nom</th>
                    <th>État</th>
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
                            ${task.officialNumber}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>${task.number}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>${task.name}</td>
                        <td onclick="document.location='${task.url}'" class='rowlink'>
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
                            ${task.officialNumber}
                            % if task.invoice:
                                (lié à la facture ${task.invoice.officialNumber})
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
