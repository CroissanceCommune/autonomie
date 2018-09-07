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
<%namespace file="/base/utils.mako" import="company_disabled_msg" />
<%block name="mainblock">
<div class='row'>
    <div class='col-md-2'>
    % if user.login:
        % if user.login.active:
            <i class='fa fa-lock fa-3x fa-border text-success' style='vertical-align:middle'></i>
        %else:
            <i class='fa fa-lock fa-3x fa-border text-danger' style='vertical-align:middle'></i>
        % endif
    % else:
        <i class='fa fa-lock fa-3x fa-border' style='vertical-align:middle'></i>
    % endif
    </div>
% if request.has_permission('edit.login'):
    <div class='col-md-10'>
    % if user.login:
        % if user.login.active:
        <span class='text-success'>
            Ce compte dispose d'identifiants
            <strong>l'utilisateur peut se connecter à Autonomie</strong>
        </span>
        <div>
            <a class='btn btn-default'
                href="${request.route_path('/users/{id}/login', id=user.id)}"
                >
                <i class='fa fa-search'></i>&nbsp;Voir
            </a>
        </div>
        % else:
        <span class='text-danger'>
            Les identifiants de ce compte sont désactivés
            <strong>
            l'utilisateur ne peut pas se connecter à Autonomie
            </strong>
        </span>
        % endif
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
% elif request.has_permission('set_email.user'):
    <div class='col-md-10'>
        <a
            class='btn btn-default'
            href="${request.route_path('/users/{id}/myaccount', id=request.context.id)}"
            >
            <i class='fa fa-pencil'></i>&nbsp;Modifier mes informations
        </a>
    % if request.has_permission('set_password.login') and user.login:
        <a
            class='btn btn-default'
            href="${request.route_path('/users/{id}/login/set_password', id=request.context.id)}"
            >
            <i class='fa fa-lock'></i>&nbsp;Changer mon mot de passe
        </a>
    % endif
    </div>
% endif
</div>
<hr />


% if request.has_permission('admin.company'):
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
            % if not company.active:
            ${company_disabled_msg()}
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
    <em>Ce compte n'est rattaché à aucune entreprise</em>
% endif
    </div>
</div>
<hr />
% endif


% if request.has_permission('view.userdatas'):
<div class='row'>
    % if user.userdatas:
    <div class='col-md-2'>
        <i
            class='fa fa-id-card-o fa-3x fa-border text-success'
            style='vertical-align:middle'></i>
    </div>
    <div class='col-md-10'>
    <div class='text-success'>Une fiche de gestion sociale est associée à ce compte</div>
    <a class='btn btn-default'
        href="${request.route_path('/users/{id}/userdatas/edit', id=user.id)}"
        >
        <i class='fa fa-search'></i>&nbsp;Voir
    </a>
    % else:
    <div class='col-md-2'>
        <i
            class='fa fa-id-card-o fa-3x fa-border'
            style='vertical-align:middle'></i>
    </div>
    <div class='col-md-10'>
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

% if request.has_permission('view.trainerdatas'):
<div class='row'>
    % if user.trainerdatas:
    <div class='col-md-2'>
        <i
            class='fa fa-graduation-cap fa-3x fa-border text-success'
            style='vertical-align:middle'></i>
    </div>
    <div class='col-md-10'>
    % if user == request.user:
    <a class='btn btn-default'
        href="${request.route_path('/users/{id}/trainerdatas/edit', id=user.id)}"
        >
        <i class='fa fa-search'></i>&nbsp;Voir ma fiche formateur
    </a>
    % else:
    <div class='text-success'>Une fiche formateur est associée à ce compte</div>
    <a class='btn btn-default'
        href="${request.route_path('/users/{id}/trainerdatas/edit', id=user.id)}"
        >
        <i class='fa fa-search'></i>&nbsp;Voir
    </a>
    % endif
    </div>
    % elif request.has_permission('add.trainerdatas'):
    <div class='col-md-2'>
        <i
            class='fa fa-graduation-cap fa-3x fa-border'
            style='vertical-align:middle'></i>
    </div>
    <div class='col-md-10'>
        <em>Aucune fiche formateur n'est associée à ce compte</em>&nbsp;
        <a
            class='btn btn-primary'
            href="${request.route_path('/users/{id}/trainerdatas/add', id=user.id)}"
            >
            <i class='fa fa-plus-circle'></i>&nbsp;Créer une fiche formateur
        </a>
    % endif
</div>
</div>
% endif
</%block>
