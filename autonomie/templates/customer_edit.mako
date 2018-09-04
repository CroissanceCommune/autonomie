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
<%block name='content'>
% if request.is_popup:
<div class='text-center'>
    <h2>
    Modification du client ${request.context.label}
    <br />
    <small>Activité : ${request.context.company.name}</small>
    </h2>
</div>
<hr />
% endif
<div class='row'>
    <div class="col-md-9">
        <div class='panel panel-default page-block'>
        <div class='panel-heading'>
        ${title}
        </div>
        <div class='panel-body'>
        ${form|n}
        </div>
        </div>
    </div>
    <div class='col-md-3'>
        <div class='panel panel-default page-block'>
        <div class='panel-heading'>
        Codes client utilisés
        </div>
        <div class='panel-body'>
        <ul>
            % for customer in customers:
                <li>
                ${customer.code.upper()} (${customer.label})
                </li>
            % endfor
        </ul>
        </div>
        </div>
    </div>
</div>
</%block>
