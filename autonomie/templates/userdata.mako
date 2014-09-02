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
<%block name="content">
<% userdata = request.context %>
<div class='well'>
% if getattr(userdata, "user_id", None) is not None and userdata.__name__ == 'userdatas':
        Ces données sont associées à un compte utilisateur : <a href='${request.route_path("user", id=userdata.user_id)}'>Voir</a>
<% del_url = request.route_path('userdata', id=userdata.id, _query=dict(action="delete")) %>
<% del_msg = u'Êtes vous sûr de vouloir supprimer les données de cette personne ?'
if userdata.user is not None:
    del_msg += u' Le compte associé sera également supprimé.'
    del_msg += u" Cette action n'est pas réversible."
%>
<a class='btn pull-right' href="${del_url}" title="Supprimer ces données" onclick="return confirm(\"${del_msg}\");">
    <i class="icon icon-trash"></i>
    Supprimer les données
</a>
% endif
</div>

<ul class='nav nav-tabs'>
    <li class='active'>
    <a href="#tab1" data-toggle='tab'>
        Informations sociales
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
        </a>
        </li>
    % endif
        <li>
        <a href="#tab4" data-toggle='tab'>
            Génération de documents
        </a>
        </li>
</ul>
<div class='tab-content'>
    <div class='tab-pane active' id='tab1'>
        ${form|n}
    </div>
    % if doctypes_form is not UNDEFINED:
    <div class='tab-pane' id='tab2'>
        <div class='span2'>
        </div>
        <div class='span8'>
            ${doctypes_form.render()|n}
        </div>
    </div>
    % endif
    % if account_form is not UNDEFINED and account_form is not None:
        <div class='tab-pane' id='tab3'>
            ${account_form.render()|n}
        </div>
    % endif
    <div class='tab-pane' id='tab4'>
        % for doctemplate in doctemplates:
            <% url = request.route_path('userdata', id=userdata.id, _query=dict(template_id=doctemplate.id, action="py3o")) %>
            <a href="${url}">
                ${doctemplate.description} ( ${doctemplate.name} )
            </a>
        % endfor
    </div>
</div>
</%block>
