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
<%namespace file="/base/utils.mako" import="format_company" />
<%block name='content'>
<div class='row'>
    <div class='col-md-5'>
        <div class='well'>
            <div class='row'>
                <div class='col-md-2'>
                    <i class='fa fa-4x fa-user'></i>
                </div>
                <div class='col-md-10'>
            <dl class="dl-horizontal">
                % if request.has_permission('view_user'):
                    <dt>Identifiant</dt>
                    <dd>${user.login}</dd>
                % endif
                % for label, value in ((u"Nom", user.lastname), (u"Prénom", user.firstname)):
                    %if value:
                        <dt>${label}</dt>
                        <dd>${value}</dd>
                    % endif
                % endfor
                <dt>E-mail</dt><dd>${format_mail(user.email)}</dd>
                % if request.has_permission('view_userdatas') and request.context.userdatas is not None:
                    <dt>Informations sociales</dt>
                    <dd>
                        <a href="${request.route_path('userdata', id=request.context.userdatas.id)}">Voir</a>
                    </dd>
                % endif
            </dl>

% if not user.enabled():
    <span class='label label-warning'>Ce compte a été désactivé</span>
% endif
</div>
</div>
        </div>
    </div>
    <div class='col-md-6 col-md-offset-1'>
        <div class='well'>
            % if len(user.companies) <= 1:
                <h3>Entreprise</h3>
            %else:
                <h3>Entreprises</h3>
            % endif
            <br />
            % for company in user.companies:
                ${format_company(company)}
                % if not company.enabled():
                    <span class='label label-warning'>Cette entreprise a été désactivée</span>
                % endif
            % endfor
        </div>
    </div>
</div>
</%block>

