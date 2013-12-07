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

<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='row-fluid'>
% if companies:
    <ul class="thumbnails">
        % for company in companies:
        <li class="span4">
        <div class="thumbnail">
            <img src="/assets/${company.get_logo_filepath()}" title="${company.name}" alt="" style="max-height:200px;"/>
            <div class="caption">
                <h3>${company.name}</h3>
                <p>
                    ${company.goal}
                </p>
                <a class="btn btn-primary" href="${company.url}" title="Accéder au gestionnaire de ${company.name}">
                    Accéder au gestionnaire de ${company.name} >>>
                </a>
            </div>
        </div>
        </li>
    % endfor
</ul>
%else:
    <strong>Aucune entreprise n'a été configurée pour ce compte</strong>
% endif
</div>
</%block>
