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
    company View page
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_company" />
<%block name='content'>
<div class='row'>
<div class='col-md-3 col-xs-12'>
% if request.has_permission('edit_company'):
    <h3 class='text-center'>Actions</h3>
    <a
        class='btn btn-default btn-block'
        href="${request.route_path('company', id=request.context.id, _query={'action': 'edit'})}"
        ><i class='glyphicon glyphicon-pencil'></i>&nbsp;Modifier
    </a>
% endif
% if request.has_permission('admin_company'):
    % if request.context.archived:
    <% _query = dict(action="enable") %>
    <% label = u"Désarchiver" %>
    % else :
    <% _query = dict(action="disable") %>
    <% label = u"Archiver" %>
    % endif
    <a
        class='btn btn-default btn-block'
        href="${request.route_path('company', id=request.context.id, _query=_query)}"
        ><i class='glyphicon glyphicon-book'></i>&nbsp;${label}
    </a>
% endif
</div>
<div class="col-md-9">
    <div class='panel panel-default page-block'>
        <div class='panel-heading'>
        Informations générales
        </div>
        <div class='panel-body'>
        ${format_company(company)}
        % if not company.enabled():
            <span class='label label-warning'>Cette entreprise a été désactivée</span>
        % endif
    %for link in link_list:
        <p>${link.render(request)|n}</p>
    %endfor
        </div>
    </div>
    <div class='panel panel-default page-block'>
        <div class='panel-heading'>
        Employé(s
        </div>
        <div class='panel-body'>
        % for user in company.employees:
            % if getattr(user, 'userdatas', None) and api.has_permission('view_userdatas', request.context):
                <% url = request.route_path('userdata', id=user.userdatas.id) %>
            % else:
                <% url = request.route_path('user', id=user.id) %>
            % endif

            <a href="${url}" title='Voir ce compte'>
                <i class='glyphicon glyphicon-user'></i>&nbsp;${api.format_account(user)}
            </a>
            <br />
        % endfor
        % if len(company.employees) == 0:
            Aucun entrepreneur n'est associé à cette entreprise
        % endif
        </div>
    </div>
</div>
</div>
</%block>
