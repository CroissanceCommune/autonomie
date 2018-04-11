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
<%block name='afteradminmenu'>
    <div class='alert alert-info'>
    Les grilles de frais kilométriques sont configurées de manière annuelle.<br />
    Choisissez l'année que vous voulez administrer.<br />
    Note : Il est possible de dupliquer les types de frais d'une année vers l'autre.
    </div>
</%block>
<%block name='content'>
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
        <div class='page-block panel panel-default'>
        <div class='panel-heading'>
        Choisir une année
        </div>
        <div class='panel-body'>
            <div class='text-center'>
                <div class='btn-group'>
                % for year in years:
                    <a
                        class='btn btn-default'
                        href="${request.route_path(admin_path, year=year)}"
                        >
                        ${year}
                    </a>
                 % endfor
                 </div>
            </div>
            </div>
        </div>
    </div>
</div>
</%block>
