<%doc>
    * Copyright (C) 2012-2016 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
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
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name="mainblock">
    <table class="table table-striped table-condensed table-hover">
        <thead>
            <th>Nom</th>
            <th>Adresse e-mail</th>
            <th>Entrepreneur(s)</th>
            <th style="text-align:center">Actions</th>
        </thead>
        <tbody>
            % for company in companies:
                <% url = request.route_path('company', id=company.id) %>
                <% onclick = "document.location='{url}'".format(url=url) %>
                % if not company.enabled():
                    <tr class="danger">
                % else:
                    <tr>
                % endif
                    <td onclick="${onclick}" class="rowlink">
                        ${company.name} ( ${company.code_compta} )
                        % if not company.enabled():
                        <span class='text-danger'>
                        <i class='fa fa-warning'></i>&nbsp;
                               cette entreprise est désactivée
                                </span>
                        % endif
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        ${company.email}
                    </td>
                    <td onclick="${onclick}" class="rowlink">
                        <ul>
                            % for employee in company.employees:
                                <li>
                                <a href="${request.route_path('/users/{id}', id=employee.id)}">
                                    ${api.format_account(employee)}
                                    </a>
                                </li>
                            % endfor
                        </ul>
                    </td>
                    <td class='actions'>
                        ${table_btn(url, u"Voir", u"Modifier l'entreprise", icon='glyphicon glyphicon-search')}
                        <% url = request.route_path('company', id=company.id, _query=dict(action='edit')) %>
                        ${table_btn(url, u"Modifier", u"Modifier l'entreprise", icon='glyphicon glyphicon-pencil')}

                        % if len(company.employees) > 1:
                            <% url = request.route_path('company', id=company.id, _query=dict(action="remove", uid=user.id)) %>
                            <% msg = u"{0} n\\'aura plus accès aux données de l\\'entreprise {1}. Êtes-vous sûr de vouloir continuer ?".format(api.format_account(user), company.name) %>

                            ${table_btn(url, \
                            u"Retirer",
                            u"Retirer %s de cette entreprise" % user.label,
                            onclick="return confirm('%s');" % msg,
                            icon="link",
                            css_class="btn-warning")}

                        % endif

                        % if company.enabled():
                            <% url = request.route_path('company', id=company.id, _query=dict(action="disable")) %>
                            <% msg = u"Cette entreprise n\\'apparaîtra plus dans les listings de factures. Êtes-vous sûr de vouloir continuer ?" %>
                            ${table_btn(url, \
                            u"Désactiver", \
                            u"désactiver l'entreprise", \
                            icon='glyphicon glyphicon-book', \
                            onclick="return confirm('%s');" % msg,
                            css_class="btn-danger")}
                        % else:
                            <% url = request.route_path('company', id=company.id, _query=dict(action="enable")) %>
                            ${table_btn(url, \
                            u"Activer", \
                            u"Activer l'entreprise", \
                            icon='glyphicon glyphicon-book', \
                            css_class="btn-success")}
                        % endif
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>
    <a href="${request.route_path('/users/{id}/companies/associate', id=user.id)}"
        class='btn btn-primary'>
        <i class="glyphicon glyphicon-plus"></i>
        Associer à une entreprise existante dans Autonomie
    </a>
    <a href="${request.route_path('companies', _query=dict(action='add', user_id=user.id))}"
        class='btn btn-primary'>
        <i class="glyphicon glyphicon-plus"></i>
        Associer à une nouvelle entreprise
    </a>
</%block>
