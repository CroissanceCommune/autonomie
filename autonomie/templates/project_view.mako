<%inherit file="base.mako"></%inherit>
<%namespace file="base/utils.mako" import="print_date" />
<%namespace file="base/utils.mako" import="address" />
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a class="btn-primary" title='Éditer les informations de ce client'
        href='${request.route_path("company_project", cid=company.id, id=project.id, _query=dict(action="edit"))}'>
        Éditer
    </a>
    </li>
    <li>
    <a class="btn-primary" title='Revenir à la liste des clients'  href='${request.route_path("company_projects", cid=company.id)}'>
        Revenir à la liste
    </a>
    </li>
    <li>
    <a class="btn-primary" title='Afficher le détail'  href="#" data-toggle='collapse' data-target='#project-description'>
        Afficher les détails
        </a>
    </li>
    <li>
        <a class="btn-primary" title='Ajouter une phase dans le projet' href="${request.route_path("company_projects", cid=company.id)}">
            Ajouter une phase
        </a>
    </li>
</ul>
</%block>
<%block name='content'>
<style>
.section-header{
    background-color: #F5F5F5;
    border-bottom: 1px solid #dedede;
    border-top: 1px solid #dedede;
    padding-left:10px;
}
</style>
<div class='container'>
    <div class='row collapse' id='project-description'>
        <div class="span2">
            <h3>Client</h3>
            ${address(project.client, "client")}
            %if project.type:
                <b>Type de projet :</b> ${project.type}
            % endif
        </div>
        <div class="span5 offset2">
            <h3>Définition du projet</h3>
            ${project.definition}
        </div>
    </div>
    %for phase in project.phases:

        % if phase.name != 'default':
            <h2 class='section-header'>
                        <a href="#" data-toggle='collapse' data-target='#phase_${phase.id}'>
                            <div>
                                ${phase.name}
                            </div>
                        </a>
                    </h2>
        % endif
        <div class="in collapse" id='phase_${phase.id}' style="margin:4px;">
            <h3 class='floatted' style="padding-right:10px">Devis</h3>
                <a class='btn' href='${request.route_path("estimations", cid=company.id, id=project.id, _query=dict(phase=phase.id))}'>
                    <span class='ui-icon ui-icon-plusthick'></span>
                </a>
        %if  phase.estimations:
            <table class='table table-striped table-condensed'>
            <thead>
                <th>Document</th>
                <th>Numéro</th>
                <th>État</th>
                <th>Date</th>
                <th>Créé par</th>
                <th>Action</th>
            </thead>
            %for estimation in phase.estimations:
                <tr>
                    <td><a href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask)}' title="Voir/éditer ce devis">${estimation.number}</a></td>
                    <td>${estimation.name}</td>
                    % if estimation.statusPersonAccount is not UNDEFINED and estimation.statusPersonAccount is not None:
                        <td>${estimation.get_status_str().format(genre='', firstname=estimation.statusPersonAccount.firstname, lastname=estimation.statusPersonAccount.lastname)}</td>
                    % else:
                        <td>${estimation.get_status_str().format(genre='', firstname="Utilisateur", lastname="Inconnu")}</td>
                    % endif
                    <td>${print_date(estimation.statusDate)}</td>
                    <td>${estimation.owner.firstname} ${estimation.owner.lastname}</td>
                    <td>
                        <a class='btn' href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask)}' title="Voir/éditer ce devis">
                            <span class='ui-icon ui-icon-pencil'></span>
                            Voir/Éditer
                        </a>
                        <a class='btn' href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask, _query=dict(pdf=True))}' title="Télécharger la version PDF">
                            PDF
                        </a>
                        <a class='btn' href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask, _query=dict(duplicate=True))}' title="Dupliquer le devis">
                            Dupliquer
                        </a>
                    </td>
                </tr>
            %endfor
        </table>
    %else:
        <div style='clear:both'>Aucun devis n'a été créé dans cette phase</div>
    %endif
    <h3 class='floatted' style='padding-right:10px;'>Facture(s)</h3>
        <a class='btn' href='${request.route_path("invoices", cid=company.id, id=project.id, _query=dict(phase=phase.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>
        </a>
        %if phase.invoices:
            <table class='table table-striped table-condensed'>
        <thead>
            <th>Document</th>
            <th>Numéro</th>
            <th>État</th>
            <th>Date</th>
            <th>Créé par</th>
            <th>Action</th>
        </thead>
            %for invoice in phase.invoices:
                <tr>
                    <td><a href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=invoice.IDTask)}' title="Voir/éditer cette facture">${invoice.number}</a></td>
                    <td>${invoice.name}</td>
                    %if invoice.statusPersonAccount is not UNDEFINED and invoice.statusPersonAccount is not None:
                        <td>${invoice.get_status_str().format(genre='e', firstname=invoice.statusPersonAccount.firstname, lastname=invoice.statusPersonAccount.lastname)}</td>
                    %else:
                        <td>${invoice.get_status_str().format(genre='e', firstname="Utilisateur", lastname="Inconnu")}</td>
                    %endif
                    <td>${print_date(invoice.statusDate)}</td>
                    <td>${invoice.owner.firstname} ${invoice.owner.lastname}</td>
                    <td>
                        <a class='btn' href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask)}' title="Voir/éditer ce devis">
                            <span class='ui-icon ui-icon-pencil'></span>
                            Voir/Éditer
                        </a>
                        <a class='btn' href='${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask, _query=dict(pdf=True))}' title="Télécharger la version PDF">
                           PDF
                        </a>
                    </td>
                </tr>
            %endfor
        </table>
        % else:
            <div style='clear:both'>Aucune facture n'a été créée dans cette phase</div>
        % endif
    </div>
    %endfor
</div>
</%block>
