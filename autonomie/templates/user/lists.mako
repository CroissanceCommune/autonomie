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

<%doc>
    Directory templates, list users and companies
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='afteractionmenu'>
<div class='page-header-block'>
    % if request.has_permission('add.userdatas'):
    <a
        class='btn btn-primary primary-action'
        href="${request.route_path('/userdatas', _query=dict(action='add'))}"
        >
        <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Ajouter un porteur de projet
    </a>
    % endif
    % if request.has_permission('add_user'):
    <a class='btn btn-default secondary-action'
    href="${request.route_path('/users', _query=dict(action='add'))}"
    >
    <i class='fa fa-user-plus'></i>&nbsp;Ajouter un permanent
    </a>
    % endif
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    <a href='#filter-form'
        data-toggle='collapse'
        aria-expanded="false"
        aria-controls="filter-form">
        <i class='glyphicon glyphicon-search'></i>&nbsp;
        Filtres&nbsp;
        <i class='glyphicon glyphicon-chevron-down'></i>
    </a>
    % if '__formid__' in request.GET:
        <div class='help-text'>
            <small><i>Des filtres sont actifs</i></small>
        </div>
        <div class='help-text'>
            <a href="${request.current_route_path(_query={})}">
                <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
            </a>
        </div>
    % endif
    </div>
    <div class='panel-body'>
    % if '__formid__' in request.GET:
        <div class='collapse' id='filter-form'>
    % else:
        <div class='in collapse' id='filter-form'>
    % endif
            <div class='row'>
                <div class='col-xs-12'>
                    ${form|n}
                </div>
            </div>
        </div>
    </div>
</div>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    ${records.item_count} Résultat(s)
    </div>
    <div class='panel-body'>
        <table class="table table-striped table-condensed">
            <thead>
                <tr>
                    <th class='col-xs-2'>${sortable("Nom", "name")}</th>
                    <th class='col-xs-1'>${sortable("E-mail", "email")}</th>
                    <th class='col-xs-5'>Entreprises</th>
                    % if request.has_permission('manage'):
                        <th class='col-xs-1 col-xs-offset-1 text-right'>Actions</th>
                    % endif
                </tr>
            </thead>
            <tbody>
                % if records:
                    % for id, user in records:
                        <% url = request.route_path('/users/{id}', id=user.id) %>
                        <tr>
                            <td>
                            <a href="${url}">
                            ${api.format_account(user)}
                            </a>
                            % if not user.login.active:
                            <span class='label label-warning pull-right'>Désactivé</span>
                            % endif
                            </td>
                            <td><a href="${url}">${user.email}</a></td>
                            <td>
                                <ul class="list-unstyled">
                                    % for company in user.companies:
                                        <% company_url = request.route_path('company', id=company.id) %>
                                        <li>
                                        <a href="${company_url}">${company.name} (<small>${company.goal}</small>)</a>
                                            % if request.has_permission('admin_company', company):
                                                % if company.enabled():
                                                    <%doc> -- <span class='label label-success pull-right'>Cette entreprise est active</span> </%doc>
                                                % else:
                                                    <span class='label label-warning pull-right'>Désactivée</span>
                                                % endif
                                            % endif
                                        </li>
                                    % endfor
                                </ul>
                            </td>
                            % if request.has_permission('manage'):
                                <td class='text-right'>
                                    <div class='btn-group'>
                                        <button
                                            type="button"
                                            class="btn btn-default dropdown-toggle"
                                            data-toggle="dropdown"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                            Actions <span class="caret"></span>
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-right">

                                        <% url = request.route_path('/users/{id}', id=user.id) %>
                                        <li><a href='${url}'>Voir le compte</a></li>
                                        <li role="separator" class="divider"></li>
                                        % if request.has_permission('add_activity'):
                                            <% activity_url = request.route_path('activities', _query={'action': 'new', 'user_id': user.id}) %>
                                            <li><a href='${activity_url}'>Nouveau rendez-vous</a></li>
                                        % endif
                                        </ul>
                                    </div>
                                </td>
                            % endif
                        </tr>
                    % endfor
                % else:
                    <tr><td colspan='3'>Aucun utilisateur n'est présent dans la base</td></tr>
                % endif
            </tbody>
        </table>
${pager(records)}
</div>
</div>
</%block>
