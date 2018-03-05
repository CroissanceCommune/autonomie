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
<%block name="mainblock">
% if request.has_permission('edit.login'):
% if user.login:
<i class='fa fa-key'></i>
    % if user.login.active:
    <h4 class='text-success'>Ce compte dispose d'identifiants <span class='help-text'>l'utilisateur peut se connecter à Autonomie</span></h4>
    % else:
    <h4 class='text-error'>Les identifiants de ce compte sont désactivés <span class='help-text'>l'utilisateur ne peut pas se connecter à Autonomie</span></h4>
    % endif
% else:
<h4 class='text-warn'>Ce compte ne dispose pas d'identifiants</h4>
<a
    class='btn btn-primary'
    href="${request.route_path('/users/{id}/login', id=user.id, _query={'action': 'add'})}"
    >
    <i class='fa fa-plus-circle'></i>&nbsp;Créer des identifiants
</a>
% endif
<hr />
% endif
% if request.has_permission('view.userdatas'):
% if user.userdatas:
<h4>Une fiche de gestion sociale est associée à ce compte</h4>
<a class='btn btn-success'
    href="${request.route_path('/users/{id}/userdatas/edit', id=user.id)}"
    >
    <i class='fa fa-search'></i>&nbsp;Voir
</a>
% else:
<h4>Aucune fiche de gestion sociale n'est associée à ce compte</h4>
<a
    class='btn btn-primary'
    href="${request.route_path('/users/{id}/userdatas/add', id=user.id)}"
    >
    <i class='fa fa-address-card'></i><i class='fa fa-plus-circle'></i>&nbsp;Créer une fiche de gestion sociale
</a>
% endif
<hr />
% endif

% if user.companies:
    % if len(user.companies) == 1:
        <h4>Ce compte est rattaché à l'entreprise
        <a
            href="${request.route_path('company', id=user.companies[0].id)}"
            title="Voir l'entreprise">
        ${user.companies[0].name}
        </a>
        </h4>
    % else:
        Ce compte est rattaché aux entreprises suivantes
        <ul>
        % for company in user.companies:
        % if company.enabled():
        <li>
            <h4>
            <a
                href='${request.route_path('company', id=company.id)}'
                title="Voir l'entreprise"
            >
                ${company.name}
            </a>
            </h4>
        </li>
        % endif
        % endfor
        </ul>
    % endif
% else:
    Ce compte n'est rattaché à aucune entreprise
% endif
</%block>
