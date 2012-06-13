<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='container'>
    <ul class="row">
        <div class='span2'>
            <h3>Entreprise</h3>
            <dl>
                % for label, value in ((u"Nom de l'entreprise", client.name), (u"Code", client.id), (u"TVA intracommunautaire", client.intraTVA)):
                    %if value:
                        <dt>${label}</dt>
                        <dd>${value}</dd>
                    % endif
                % endfor
            </dl>
        </div>
        <div class="span3 offset1">
            <h3>Contact principal</h3>
            <strong>${client.contactLastName} ${client.contactFirstName}</strong>
            <br />
            % if client.address:
                <address>
                    ${client.address}<br />
                    ${client.zipCode} ${client.city}
                    % if client.country and client.country!= 'France':
                        <br />${client.country}
                    % endif
                </address>
            %else:
                Aucun adresse connue
                <br />
            %endif
            <dl>
                <dt>E-mail</dt>
                <dd>
                    %if client.email:
                        <address>
                            ${client.email}
                        </address>
                    % else:
                        Aucune adresse connue
                    % endif
                </dd>
                <dt>Téléphone</dt>
                <dd>
                    %if client.phone:
                        ${client.phone}
                    %else:
                        Aucun numéro connu
                    %endif
                </dd>
            </dl>
        </div>
        <div class='span5 offset1'>
            % if client.comments:
                <h3>Commentaires</h3>
                <blockquote style='padding:15px;margin-top:25px;border:1px solid #eee;'>
                    ${client.comments}
                </blockquote>
            %else :
                Aucun commentaire
            % endif
        </div>
    </div>
    <div class='row'>
    </div>
    <h2>Projets</h2>
    <div class='row'>
        %if client.projects:
        <table class="table table-striped table-condensed">
            <thead>
                <tr>
                    <th>Code</th>
                    <th>Nom</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                % for project in client.projects:
                    %if project.is_archived():
                        <tr class='tableelement' style='background-color:#999' id="${project.id}">
                    %else:
                        <tr class='tableelement' id="${project.id}">
                    %endif
                        <td>${project.code}</td>
                        <td>${project.name}
                            %if project.is_archived():
                                (ce projet a été archivé)
                            %endif
                        </td>
                        <td>
                        <div class='btn-group'>
                            <a class='btn' href='${request.route_path("company_project", id=project.id)}'>
                                <span class='ui-icon ui-icon-pencil'></span>
                                Voir
                            </a>
                            <a class='btn' href='${request.route_path("estimations", id=project.id)}'>
                                <span class='ui-icon ui-icon-plusthick'></span>
                                Devis
                            </a>
                            <a class='btn' href='${request.route_path("invoices", id=project.id)}'>
                                <span class='ui-icon ui-icon-plusthick'></span>
                                Facture
                            </a>
                            %if not project.is_archived():
                                <a class='btn'
                                    href='${request.route_path("company_project", id=project.id, _query=dict(action="archive"))}'
                                    onclick="return confirm('Êtes-vous sûr de vouloir archiver ce projet ?');">
                                    <span class='ui-icon ui-icon-folder-collapsed'></span>
                                    Archiver
                                </a>
                            %elif project.is_deletable():
                                <a class='btn'
                                    href='${request.route_path("company_project", id=project.id, _query=dict(action="delete"))}'
                                    onclick="return confirm('Êtes-vous sûr de vouloir supprimer définitivement ce projet ?');">
                                    <span class='ui-icon ui-icon-trash'></span>
                                    Supprimer
                                </a>
                            %endif
                        </div>
                        </td>
                    </tr>

                %endfor
            </tbody>
        </table>
    %else:
        Aucun projet n'a été initié avec ce client
    %endif
    </div>
</div>
</%block>
