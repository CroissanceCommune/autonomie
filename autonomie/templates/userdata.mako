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
% if getattr(request.context, "user_id", None) is not None and request.context.__name__ == 'userdata':
    <div class='well'>
        Ces données sont associées à un compte utilisateur : <a href='${request.route_path("user", id=request.context.user_id)}'>Voir</a>
    </div>
% endif
<ul class='nav nav-tabs'>
    <li class='active'>
    <a href="#form1" data-toggle='tab'>
        Formulaire de saisie
    </a>
    </li>
    % if doctypes_form is not UNDEFINED:
        <li>
        <a href="#form2" data-toggle='tab'>
            Documents sociaux
        </a>
        </li>
    % endif
</ul>
<div class='tab-content'>
    <div class='tab-pane active' id='form1'>
        ${form|n}
    </div>
    % if doctypes_form is not UNDEFINED:
    <div class='tab-pane' id='form2'>
        ${doctypes_form.render()|n}
    </div>
    % endif
</div>
</%block>
