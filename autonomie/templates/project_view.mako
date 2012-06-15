<%inherit file="base.mako"></%inherit>
<%namespace file="base/utils.mako" import="print_date" />
<%namespace file="base/utils.mako" import="address" />
<%block name='content'>
    <div class='row collapse' id='project-addphase'>
        <div class='span4'>
            <h3>Ajouter une phase</h3>
            <form class='navbar-form' method='POST' action="${request.route_path('company_project', id=project.id, _query=dict(action='addphase'))}">
                <input type='text' name='phase' />
                <button class='btn btn-primary' type='submit' name='submit' value='addphase'>Valider</button>
            </form>
            <br />
        </div>
    </div>
    <div class='row collapse' id='project-description'>
        <div class="span2">
            <h3>Client</h3>
            ${address(project.client, "client")}
            %if project.type:
                <b>Type de projet :</b> ${project.type}
            % endif
            <a class="btn btn-primary" title='Éditer les informations de ce client'
                href='${request.route_path("company_project", id=project.id, _query=dict(action="edit"))}'>
                Éditer
            </a>
            <br />
            <br />
        </div>
        <div class="span5 offset2">
            <h3>Définition du projet</h3>
            ${project.definition}
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
                ##<th>Date</th>
                ##<th>Créé par</th>
                <th>Action</th>
            </thead>
            %for estimation in phase.estimations:
                <tr>
                    <td><a href='${request.route_path("estimation", id=estimation.IDTask)}' title="Voir/éditer ce devis">${estimation.number}</a></td>
                    <td>${estimation.name}</td>
                    <td>${estimation.get_status_str('estimation')}</td>
                    ##    <td>${print_date(estimation.statusDate)}</td>
                    ##<td>${estimation.owner.firstname} ${estimation.owner.lastname}</td>
                    <td>
                        <a class='btn' href='${request.route_path("estimation", id=estimation.IDTask)}' title="Voir/éditer ce devis">
                            <span class='ui-icon ui-icon-pencil'></span>
                            Voir/Éditer
                        </a>
                        <a class='btn' href='${request.route_path("estimation", id=estimation.IDTask, _query=dict(view="pdf"))}' title="Télécharger la version PDF">
                            PDF
                        </a>
                        <a class='btn' href='${request.route_path("estimation", id=estimation.IDTask, _query=dict(action="duplicate"))}' title="Dupliquer le devis">
                            Dupliquer
                        </a>
                        %if estimation.is_deletable():
                            <a class='btn'
                                href='${request.route_path("estimation", id=estimation.IDTask, _query=dict(action="delete"))}'
                                title="Supprimer le devis"
                                onclick="return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');">
                                Supprimer
                            </a>
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
        <a class='btn' href='${request.route_path("invoices", id=project.id, _query=dict(phase=phase.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>
        </a>
        %if phase.invoices:
            <table class='table table-striped table-condensed'>
        <thead>
            <th>Document</th>
            <th>Nom</th>
            <th>État</th>
            ##<th>Date</th>
            ##<th>Créé par</th>
            <th>Action</th>
        </thead>
            %for invoice in phase.invoices:
                <tr>
                    <td><a href='${request.route_path("invoice", id=invoice.IDTask)}' title="Voir/éditer cette facture">${invoice.number}</a></td>
                    <td>${invoice.name}</td>
                    <td>${invoice.get_status_str("invoice")}</td>
                    ##      <td>${print_date(invoice.statusDate)}</td>
                    ##      <td>${invoice.owner.firstname} ${invoice.owner.lastname}</td>
                    <td>
                        <a class='btn' href='${request.route_path("invoice", id=invoice.IDTask)}' title="Voir/éditer ce devis">
                            <span class='ui-icon ui-icon-pencil'></span>
                            Voir/Éditer
                        </a>
                        <a class='btn' href='${request.route_path("invoice", id=invoice.IDTask, _query=dict(view="pdf"))}' title="Télécharger la version PDF">
                           PDF
                        </a>
                    </td>
                </tr>
            %endfor
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
