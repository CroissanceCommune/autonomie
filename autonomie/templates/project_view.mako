<%inherit file="base.mako"></%inherit>
<%namespace file="base/utils.mako" import="print_date" />
<%namespace file="base/utils.mako" import="address" />
<%namespace file="base/utils.mako" import="table_btn" />
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
                    <h3>Client</h3>
                    ${address(project.client, "client")}
                </div>
                <div class="span3">
                    <dl>
                        %if project.type:
                            <dt>Type de projet :</dt> <dd>${project.type}</dd>
                        % endif
                    </dl>
                </div>
            </div>
                <h3>Définition du projet</h3>
                <p>
                    ${project.definition}
                </p>
                <br />
                <a class="btn btn-primary" title='Éditer les informations de ce client'
                    href='${request.route_path("project", id=project.id, _query=dict(action="edit"))}'>
                    Éditer
                </a>
            </div>
        </div>
    </div>
    <style>
        .section-header a{
            display:block;
            padding-left:10px;
            padding-bottom:5px;
            padding-top:5px;
            color:#111;
            font-weight:bold;
            vertical-align:middle;
            font-size:24px;
            text-transform:capitalize;
            }
            .section-header a:hover{
                text-decoration:none;
                color:#333;
                font-weight:bold;
                background-color:#f5f5f5;
                }
                h3.floatted{
                    font-size:16px;
                    font-weight:100;
                    }
                    .section-content{
                        margin:4px;
                        margin-left:27px;
                        padding-left:10px;
                        border-left:2px solid #d1d1d1;
                        }
                    </style>
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
                                %else:
                                    <div class="section-content" id='phase_${phase.id}'>
                                    % endif
                                    <h3 class='floatted' style="padding-right:10px;">Devis</h3>
                                    <a class='btn' href='${request.route_path("estimations", id=project.id, _query=dict(phase=phase.id))}'>
                                        <span class='ui-icon ui-icon-plusthick'></span>
                                    </a>
                                    %if  phase.estimations:
                                        <table class='table table-striped table-condensed'>
                                            <thead>
                                                <th>Document</th>
                                                <th>Nom</th>
                                                <th>État</th>
                                                <th style="text-align:center">Action</th>
                                            </thead>
                                            %for task in phase.estimations:
                                                <tr>
                                                    <% task.url = request.route_path("estimation", id=task.id) %>
                                                    <td class='rowlink' onclick="document.location='${task.url}'">${task.number}</td>
                                                    <td class='rowlink' onclick="document.location='${task.url}'">${task.name}</td>
                                                    <td class='rowlink' onclick="document.location='${task.url}'">
                                                        %if task.is_cancelled():
                                                            <span class="label label-important">
                                                                >
                                                            </span>
                                                        %elif task.is_draft():
                                                            <i class='icon icon-bold'></i>
                                                        %elif task.CAEStatus == 'geninv':
                                                            <i class='icon icon-tasks'></i>
                                                        %elif task.is_waiting():
                                                            <i class='icon icon-time'></i>
                                                        %endif
                                                        ${task.get_status_str()}
                                                    </td>
                                                    <td style="text-align:right">
                                                        ${table_btn(task.url, u"Voir/Éditer", u"Voir/éditer ce devis", u"icon-pencil")}
                                                        ${table_btn(request.route_path("estimation", id=task.id, _query=dict(view="pdf")), u"PDF", u"Télécharger la version PDF", u"icon-file")}
                                                        ${table_btn(request.route_path("estimation", id=task.id, _query=dict(action="duplicate")), u"Dupliquer", u"Dupliquer le devis", icotext="<b>x2</b>")}
                                                        %if task.is_deletable():
                                                            ${table_btn(request.route_path("estimation", id=task.id, _query=dict(action="delete")), u"Supprimer", u"Supprimer le devis", icon="icon-trash", onclick=u"return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');")}
                                                        %endif
                                                    </td>
                                                </tr>
                                            %endfor
                                        </table>
                                    %else:
                                        <div style='clear:both'>Aucun devis n'a été créé
                                            %if not phase.is_default():
                                                dans cette phase
                                            %endif
                                        </div>
                                    %endif
                                    <h3 class='floatted' style='padding-right:10px;font-weight:100;'>Facture(s)</h3>
                                    <a class='btn' href='${request.route_path("project_invoices", id=project.id, _query=dict(phase=phase.id))}'>
                                        <span class='ui-icon ui-icon-plusthick'></span>
                                    </a>
                                    %if phase.invoices:
                                        <table class='table table-striped table-condensed'>
                                            <thead>
                                                <th>Numéro</th>
                                                <th>Document</th>
                                                <th>Nom</th>
                                                <th>État</th>
                                                <th style="text-align:center">Action</th>
                                            </thead>
                                            %for task in phase.invoices:
                                                <tr>
                                                    <% task.url = request.route_path("invoice", id=task.id) %>
                                                    <td onclick="document.location='${task.url}'" class='rowlink'>
                                                        ${task.officialNumber}</td>
                                                    <td onclick="document.location='${task.url}'" class='rowlink'>${task.number}</td>
                                                    <td onclick="document.location='${task.url}'" class='rowlink'>${task.name}</td>
                                                    <td onclick="document.location='${task.url}'" class='rowlink'>
                                                        %if task.is_cancelled():
                                                            <span class="label label-important">
                                                                >
                                                            </span>
                                                        %elif task.is_paid():
                                                            <i class='icon icon-ok'></i>
                                                        %elif task.is_draft():
                                                            <i class='icon icon-bold'></i>
                                                        %elif task.is_waiting():
                                                            <i class='icon icon-time'></i>
                                                        %endif
                                                        ${task.get_status_str()}
                                                    </td>
                                                    <td style="text-align:right">
                                                        ${table_btn(task.url, u"Voir/Éditer", u"Voir/éditer cette facture", u"icon-pencil")}
                                                        ${table_btn(request.route_path("cancelinvoice", id=task.id, _query=dict(view="pdf")), u"PDF", u"Télécharger la version PDF", u"icon-file")}
                                                    </td>
                                                </tr>
                                            %endfor
                                            % for task in phase.cancelinvoices:
                                                <tr>
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
                                                        %if task.is_paid():
                                                            <i class='icon icon-ok'></i>
                                                        %elif task.is_draft():
                                                            <i class='icon icon-bold'></i>
                                                        %endif
                                                        ${task.get_status_str()}</td>
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
