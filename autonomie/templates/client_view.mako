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
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='content'>
<div class="row">
    <div class='span3'>
        <div class='well'>
            <h3>Entreprise ${client.name.upper()}</h3>
            <dl>
                <% datas = ((u"Nom de l'entreprise", client.name),
                            (u"Code", client.code),
                            (u"TVA intracommunautaire", client.intraTVA),
                            (u"Compte CG", client.compte_cg),
                            (u"Compte Tiers", client.compte_tiers),) %>
                 % for label, value in datas :
                    %if value:
                        <dt>${label}</dt>
                        <dd>${value}</dd>
                    % endif
                % endfor
            </dl>
            <h3>Contact principal</h3>
            <strong>${api.format_name(client.contactFirstName, client.contactLastName)}</strong>
            % if client.function:
                <div>Fonction: ${format_text(client.function)}</div>
            % endif
            <br />
            % if client.address:
                <address>
                    ${format_text(client.full_address)}
                </address>
            %else:
                Aucun adresse connue
                <br />
            %endif
            <dl>
                <dt>E-mail</dt>
                <dd>
                    %if client.email:
                        ${format_mail(client.email)}
                    % else:
                        Aucune adresse connue
                    % endif
                </dd>
                <dt>Téléphone</dt>
                <dd>
                    %if client.phone:
                        ${format_phone(client.phone)}
                    %else:
                        Aucun numéro connu
                    %endif
                </dd>
                <dt>Fax</dt>
                <dd>
                    %if client.fax:
                        ${format_phone(client.fax)}
                    % else:
                        Aucun numéro de fax connu
                    % endif
                </dd>
            </dl>
        </div>
    </div>
    <div class='span9'>
        <h2>Projets</h2>
        <a class='btn' href='${request.route_path("company_projects", id=client.company.id, _query=dict(action="add", client=client.id))}'>
            <span class='ui-icon ui-icon-plusthick'></span>Nouveau projet
        </a>
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
                                        <a class='btn' href='${request.route_path("project", id=project.id)}'>
                                            <span class='ui-icon ui-icon-pencil'></span>
                                            Voir
                                        </a>
                                        %if not project.is_archived():
                                            <a class='btn' href='${request.route_path("project_estimations", id=project.id)}'>
                                                <span class='ui-icon ui-icon-plusthick'></span>
                                                Devis
                                            </a>
                                            <a class='btn' href='${request.route_path("project_invoices", id=project.id)}'>
                                                <span class='ui-icon ui-icon-plusthick'></span>
                                                Facture
                                            </a>
                                            <a class='btn'
                                                href='${request.route_path("project", id=project.id, _query=dict(action="archive"))}'
                                                onclick="return confirm('Êtes-vous sûr de vouloir archiver ce projet ?');">
                                                <span class='ui-icon ui-icon-folder-collapsed'></span>
                                                Archiver
                                            </a>
                                        %elif project.is_deletable():
                                            <a class='btn'
                                                href='${request.route_path("project", id=project.id, _query=dict(action="delete"))}'
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
<div class='row'>
    <div class='span12'>
        <div class='well'>
            % if client.comments:
                <h3>Commentaires</h3>
                ${format_text(client.comments)|n}
            %else :
                Aucun commentaire
            % endif
        </div>
    </div>
</div>
</%block>
