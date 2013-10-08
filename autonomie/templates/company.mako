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
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_company" />
<%block name='content'>
<div class='row'>
    <div class="span4 offset1">
        <div class='well'>
            ${format_company(company)}
        %for link in link_list:
            <p>${link.render(request)|n}</p>
        %endfor
        </div>
    </div>
    <div class="span6">
        <div class='well'>
        %if len(company.employees) > 1:
            <h3>Employé(s)</h3>
        %elif len(company.employees) == 1:
            <h3>Employé</h3>
        %else:
            <h3>Il n'y a aucun compte associé à cette entreprise</h3>
        %endif

        % for empl in company.employees:
            <a href="${request.route_path('user', id=empl.id)}" title='Voir ce compte'>
                <i class='icon-user'></i>${empl.lastname} ${empl.firstname}
            </a>
            <br />
            <br />
        % endfor
    </div>
    </div>
</div>
</%block>
