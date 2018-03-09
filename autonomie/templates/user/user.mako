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
<div class='row'>
<div class='col-md-2'>
<i class='fa fa-lock fa-3x fa-border' style='vertical-align:middle'></i>
</div>
<div class='col-md-10'>

% if user.login:
    <div>
    % if user.login.active:
    <span class='text-success'>
        Ce compte dispose d'identifiants
        <b>l'utilisateur peut se connecter à Autonomie</b>
    </span>
    % else:
    <span class='text-warning'>
        Les identifiants de ce compte sont désactivés
        <b>
        l'utilisateur ne peut pas se connecter à Autonomie
        </b>
    </span>
    % endif
    </div>
    <a class='btn btn-default'
        href="${request.route_path('/users/{id}/login', id=user.id)}"
        >
        <i class='fa fa-search'></i>&nbsp;Voir
    </a>
% else:
    <em>Ce compte ne dispose pas d'identifiants</em><&nbsp;
    <a
    class='btn btn-primary'
    href="${request.route_path('/users/{id}/login', id=user.id, _query={'action': 'add'})}"
    >
        <i class='fa fa-plus-circle'></i>&nbsp;Créer des identifiants
    </a>
% endif
</div>
</div>
<hr />
% endif


% if request.has_permission('edit.company'):
<div class='row'>
<div class='col-md-2'>
<i class='fa fa-building fa-3x fa-border' style='vertical-align:middle'></i>
</div>
<div class='col-md-10'>
% if user.companies:
    % if len(user.companies) == 1:
        <span>Ce compte est rattaché à l'entreprise
        <a
            href="${request.route_path('company', id=user.companies[0].id)}"
            title="Voir l'entreprise">
        ${user.companies[0].name}
        </a>
        </span>
    % else:
        Ce compte est rattaché aux entreprises suivantes&nbsp;
        <ul>
        % for company in user.companies:
        <li>
            <a
                href='${request.route_path('company', id=company.id)}'
                title="Voir l'entreprise"
            >
                ${company.name}
            </a>
            % if not company.enabled():
            <span class='text-danger'><i class='fa fa-warning'></i>&nbsp;cette entreprise est désactivée</span>
            % endif
        </li>
        % endfor
        </ul>
        <a class='btn btn-default'
            href="${request.route_path('/users/{id}/companies', id=user.id)}"
            >
            <i class='fa fa-search'></i>&nbsp;Voir
        </a>
    % endif
% else:
    Ce compte n'est rattaché à aucune entreprise
% endif
</div>
</div>
<hr />
% endif


% if request.has_permission('view.userdatas'):
<div class='row'>
<div class='col-md-2'>
<i class='fa fa-id-card-o fa-3x fa-border' style='vertical-align:middle'></i>
</div>
<div class='col-md-10'>

    % if user.userdatas:
    <div class='text-success'>Une fiche de gestion sociale est associée à ce compte</div>
    <a class='btn btn-default'
        href="${request.route_path('/users/{id}/userdatas/edit', id=user.id)}"
        >
        <i class='fa fa-search'></i>&nbsp;Voir
    </a>
    % else:
    <em>Aucune fiche de gestion sociale n'est associée à ce compte</em>&nbsp;
    <a
        class='btn btn-primary'
        href="${request.route_path('/users/{id}/userdatas/add', id=user.id)}"
        >
        <i class='fa fa-plus-circle'></i>&nbsp;Créer une fiche de gestion sociale
    </a>
    % endif
</div>
</div>
<hr />
% endif
</%block>
