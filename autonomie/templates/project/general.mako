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
<%namespace file="/base/utils.mako" import="format_text" />
<%block name="mainblock">
<h3>Client(s)</h3>
% for customer in project.customers:
    <div class=''>
        <a href="${request.route_path('customer', id=customer.id, _query={'action': 'edit'})}"
            class='btn btn-default btn-small pull-right'
            title="Modifier ce client">
            <i class='glyphicon glyphicon-pencil'></i> Modifier
        </a>
        <address>
            ${format_text(customer.full_address)}
        </address>
        <div class='clearfix'></div>
        <hr />
    </div>
% endfor
<h3>Informations générales</h3>
<dl>
    <dt>Type de projet :</dt><dd>${project.project_type.label}</dd>
    % if project.subtypes:
        <dt>Types d'affaire :</dt><dd>${','.join([s.label for s in project.subtypes])}</dd>
    % endif
    %if project.description:
        <dt>Description succinte :</dt> <dd>${project.description}</dd>
    % endif
    % if project.starting_date:
        <dt>Début prévu le :</dt><dd>${api.format_date(project.starting_date)}</dd>
    % endif
    % if project.ending_date:
        <dt>Livraison prévue le :</dt><dd>${api.format_date(project.ending_date)}</dd>
    % endif
</dl>
% if project.definition:
    <h3>Définition du projet</h3>
    <p>
        ${format_text(project.definition)|n}
    </p>
% endif
</div>
</%block>
