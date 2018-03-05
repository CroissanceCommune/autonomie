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
% if login is None:
<h4 class='text-warning'>
<i class='fa fa-warning'></i>&nbsp;Ce compte ne dispose pas d'identifiant
pour se connecter à Autonomie
</h4>
<a
    class='btn btn-primary primary-action'
    href="${request.route_path('/users/{id}/login', id=request.context.id, _query={'action': 'add'})}"
>
    <i class='fa fa-plus-circle'></i>&nbsp;Créer des identifiants pour ce compte
</a>
% else:
    % if request.has_permission('edit.login'):
        % if login.active:
        <h4 class='text-success'>
        <i class='fa fa-check'></i>&nbsp;Ces identifiants sont actifs
        </h4>
        <a
            href="${request.route_path('/users/{id}/login/edit', id=login.user_id)}"
            class='btn btn-default btn-primary primary-action'
            >
            <i class='fa fa-pencil'></i>&nbsp;Modifier (mot passe/identifiant)
        </a>

        <a
            href="${request.route_path('/logins/{id}', id=login.id, _query={'action': 'activate'})}"
            class='btn btn-default btn-danger'
            title="Désactiver ce compte (cet utilisateur ne pourra plus se connecter)">
            <i class='fa fa-book'></i>&nbsp;Désactiver ce compte
        </a>

        % else:
        <h4 class='text-danger'>
            <i class='fa fa-remove'></i>&nbsp;Ces identifiants ne sont pas actifs
        </h4>
        <a
            href="${request.route_path('/logins/{id}', id=login.id, _query={'action': 'activate'})}"
            class='btn btn-default'>
            <i class='fa fa-check'></i>&nbsp;Activer
        </a>
        % endif
        <div>
        <h5>Nom d'utilisateur : ${login.login}</h5>
        Fait partie des groupes
        <ul>
        % for group in login._groups:
        <li>${group.label}</li>
        % endfor
        </ul>
        </div>

    % elif request.has_permission('set_password.login'):
        <a
            href="${request.route_path('/users/{id}/login/set_password', id=_context.id)}"
            class='btn btn-primary'
            >
            <i class='fa fa-lock'></i>&nbsp;Changer mon mot de passe
        </a>
    % endif
% endif
</%block>
