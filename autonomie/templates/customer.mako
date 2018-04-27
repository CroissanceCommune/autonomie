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

<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="table_btn" />
<%block name='content'>
<div class="row">
    <div class='col-md-4'>
        <div class='panel panel-default page-block'>
        <div class='panel-heading'>
            Informations générales
        </div>
        <div class='panel-body'>
            % if customer.is_company():
                <h2>Entreprise ${customer.name.upper()}</h2>
            % else:
                <h2>${customer.get_label()}</h2>
            % endif
        <a class='btn btn-primary secondary-action'
            href='${request.route_path("customer", id=customer.id, _query=dict(action="edit"))}'>
            <i class='glyphicon glyphicon-pencil'></i>&nbsp;Modifier
        </a>
            % if customer.is_company():
                <h3>Contact principal : ${customer.get_name()}</h3>
                % if customer.function:
                <div class='row'>
                    <div class='col-xs-6'>
                        <b>Fonction</b>
                    </div>
                    <div class='col-xs-6'>
                        ${format_text(customer.function)}
                    </div>
                </div>
                % endif
            % else:
                <h3>Contact</h3>
            % endif
            <div class="row">
                <div class='col-xs-6'>
                    <b>Adresse Postale</b>
                </div>
                <div class='col-xs-6'>
                    <address>${format_text(customer.full_address)}</address>
                </div>
            </div>
            <div class="row">
                <div class='col-xs-6'>
                    <b>Addresse électronique</b>
                </div>
                <div class='col-xs-6'>
                    %if customer.email:
                        ${format_mail(customer.email)}
                    % else:
                        <i>Non renseigné</i>
                    % endif
                </div>
            </div>
            <div class="row">
                <div class='col-xs-6'>
                    <b>Téléphone portable</b>
                </div>
                <div class='col-xs-6'>
                    %if customer.mobile:
                        ${format_phone(customer.mobile)}
                    %else:
                        <i>Non renseigné</i>
                    %endif
                </div>
            </div>
            <div class="row">
                <div class='col-xs-6'>
                    <b>Téléphone</b>
                </div>
                <div class='col-xs-6'>
                    %if customer.phone:
                        ${format_phone(customer.phone)}
                    %else:
                        <i>Non renseigné</i>
                    %endif
                </div>
            </div>
            <div class="row">
                <div class='col-xs-6'>
                    <b>Fax</b>
                </div>
                <div class='col-xs-6'>
                    %if customer.fax:
                        ${format_phone(customer.fax)}
                    % else:
                        <i>Non renseigné</i>
                    % endif
                </div>
            </div>
            </div>
        </div>
            <div class='panel panel-default page-block'>
            <div class='panel-heading'>
                Informations comptables
            </div>
            <div class='panel-body'>
                % if customer.is_company():
                    <% datas = (
                    (u"TVA intracommunautaire", customer.tva_intracomm),
                    (u"Compte CG", customer.compte_cg),
                    (u"Compte Tiers", customer.compte_tiers),) %>
                %else:
                    <% datas = (
                    (u"Compte CG", customer.compte_cg),
                    (u"Compte Tiers", customer.compte_tiers),) %>
                % endif
                % for label, value in datas :
                <div class='row'>
                    <div class='col-xs-6'><b>${label}</b></div>
                        <div class='col-xs-6'>
                            % if value:
                                ${value}
                            % else:
                                <i>Non renseigné</i>
                            % endif
                        </div>
                </div>
                % endfor
            </div>
            </div>
    </div>
    <div class='col-md-8'>
    <div class='panel panel-default page-block'>
    <div class='panel-heading'>
        Projets
    </div>
    <div class='panel-body'>
        <a class='btn btn-primary primary-action'
            href='${add_project_url}'>
            <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Nouveau projet
        </a>
        %if customer.projects:
            <table class="table table-striped table-condensed">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Nom</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    % for project in customer.projects:
                        %if project.archived:
                            <tr class='tableelement' style='background-color:#999' id="${project.id}">
                            %else:
                                <tr class='tableelement' id="${project.id}">
                                %endif
                                <td>${project.code}</td>
                                <td>${project.name}
                                    %if project.archived:
                                        (ce projet a été archivé)
                                    %endif
                                </td>
                                <td>
                                    <div class='btn-group'>
                                        ${table_btn(request.route_path("/projects/{id}", id=project.id), u"Voir", "Voir ce projet", icon=u"pencil")}
                                        %if not project.archived:
                                            ${table_btn(request.route_path("/projects/{id}/estimations", id=project.id), u"Devis", "Ajouter un devis", icon=u"plus")}
                                            ${table_btn(request.route_path("/projects/{id}/invoices", id=project.id), u"Facture", "Ajouter une facture", icon=u"plus")}
                                            ${table_btn(request.route_path("/projects/{id}", id=project.id, _query=dict(action="archive")), u"Archiver", u"Archiver ce projet", onclick=u"return confirm('Êtes-vous sûr de vouloir archiver ce projet ?');", icon=u"book")}
                                        %elif api.has_permission('delete_project', project):
                                            <% del_url = request.route_path("/projects/{id}", id=project.id, _query=dict(action="delete")) %>
                                            ${table_btn(del_url,\
                                            u"Supprimer", \
                                            u"Supprimer ce projet", \
                                            onclick=u"return confirm('Êtes-vous sûr de vouloir supprimer définitivement ce projet ?');", \
                                            icon=u"trash", \
                                            css_class='btn-danger'\
                                            )}
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
    </div>
</div>
<div class='row'>
    <div class='col-md-12'>
        <hr />
        <div class=''>
            % if customer.comments:
                <h3>Commentaires</h3>
                ${format_text(customer.comments)}
            %else :
                Aucun commentaire
            % endif
        </div>
    </div>
</div>
</%block>
