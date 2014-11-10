<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
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
<%doc>
    User datas edition page
    Include two forms, one for datas edition, the other for doctypes
    registration
</%doc>
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name="content">
<% userdata = request.context %>
<div class='well'>
% if getattr(userdata, "user_id", None) is not None and userdata.__name__ == 'userdatas':
        Ces données sont associées à un compte utilisateur : <a href='${request.route_path("user", id=userdata.user_id)}'>Voir</a>
<% del_url = request.route_path('userdata', id=userdata.id, _query=dict(action="delete")) %>
<% del_msg = u'Êtes vous sûr de vouloir supprimer les données de cette personne ?'
if userdata.user is not None:
    del_msg += u' Le compte associé sera également supprimé.'
    del_msg += u" Cette action n\\'est pas réversible."
%>
<a class='btn btn-danger pull-right' href="${del_url}" title="Supprimer ces données" onclick="return confirm('${del_msg}');">
    <i class="icon icon-white icon-trash"></i>
    Supprimer les données
</a>
% endif
</div>
<% user = getattr(request.context, "user", None) %>

<ul class='nav nav-tabs'>
    <li class='active'>
    <a href="#tab1" data-toggle='tab'>
        Informations sociales
    </a>
    </li>
    <li>
        <a href="#tab4" data-toggle='tab'>
            Génération de documents
        </a>
    </li>
    % if doctypes_form is not UNDEFINED:
        <li>
        <a href="#tab2" data-toggle='tab'>
            Documents sociaux
        </a>
        </li>
    % endif
    % if account_form is not UNDEFINED and account_form is not None:
        <li>
        <a href="#tab3" data-toggle='tab'>
            Compte utilisateur
            % if user is not None and not user.enabled():
                <span class='label label-warning'>Ce compte a été désactivé</span>
            % endif
        </a>
        </li>
    % endif
</ul>
<div class='tab-content'>
    <div class='tab-pane row-fluid active' id='tab1'>
        ${form|n}
    </div>
    % if doctypes_form is not UNDEFINED:
    <div class='tab-pane row-fluid' id='tab2'>
        <div class='span8'>
            ${doctypes_form.render()|n}
        </div>
        <div class='span4'>
            <h3>Liste des documents déposés dans Autonomie</h3>
            <a class='btn btn-success'
                href="${request.route_path('userdata', id=userdata.id, _query=dict(action='attach_file'))}"
                title="Déposer un document scanné dans autonomie">
                Déposer un document
            </a>
            ${format_filelist(userdata)}
        </div>
    </div>
    % endif
    % if account_form is not UNDEFINED and account_form is not None:
        <div class='tab-pane row-fluid' id='tab3'>
            ${account_form.render()|n}
        </div>
    % endif
    <div class='tab-pane row-fluid' id='tab4'>
        <div class='row-fluid'>
            <div class='span6'>
        % for doctemplate in doctemplates:
            <% url = request.route_path('userdata', id=userdata.id, _query=dict(template_id=doctemplate.id, action="py3o")) %>
            <a class='btn btn-success' href="${url}">
                <i class="fa fa-file fa-1x"></i>
                ${doctemplate.description} ( ${doctemplate.name} )
            </a>
        % endfor
        % if doctemplates == []:
            <div class='well'>
            <i class='fa fa-question-circle fa-2x'></i>
            Vous devez déposer des modèles de document dans Autonomie pour pouvoir accéder à cet outil.
                <br />
            % if request.user.is_admin():
                <a href="${request.route_path('templates')}">Déposer de nouveau modèle de document</a>
            % else:
                Veuillez vous addresser à un administrateur.
            % endif
        </div>
        % endif
            </div>
            <div class='span6'>
                <h3>Historique des documents générés depuis Autonomie</h3>
                <span class='help-block'>
                    <i class='fa fa-question-circle fa-2x'></i>
                    Chaque fois qu'un utilisateur génère un document depuis cette page, une entrée est ajoutée à l'historique.<br />
                    Si nécessaire, pour rendre plus pertinente cette liste, vous pouvez supprimer certains entrées.
                </span>
                <table class='table table-stripped table-condensed'>
                    <thead>
                        <th>Nom du document</th>
                        <th>Généré par</th>
                        <th>Date</th>
                        <th class='text-right'>Actions</th>
                    </thead>
                    <tbody>
                        % for history in userdata.template_history:
                            <tr>
                                <td>${history.template.description}</td>
                                <td>${api.format_account(history.user)}</td>
                                <td>${api.format_datetime(history.created_at)}</td>
                                <td>
                                    <a
                                        class='btn btn-danger'
                                        href="${request.route_path('templatinghistory', id=history.id, _query=dict(action='delete'))}"
                                        ><i class='fa fa-trash fa-1x'></i>
                                        Supprimer cette entrée
                                    </a>
                                </td>
                            </tr>
                        % endfor
                        % if len(userdata.template_history) == 0:
                            <tr><td colspan='4'>Aucun document n'a été généré pour ce compte</td></tr>
                        % endif
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
</%block>
