<%doc>
    * Copyright (C) 2012-2015 Croissance Commune
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
<%block name="afteractionmenu">
<div class='page-header-block'>
    <a class='pull-right btn btn-default'
        href="${request.route_path('competence_grid', id=request.context.id, _query={'action': 'radar'})}"
        >
        <i class='fa fa-line-chart'></i>&nbsp;Voir le profil de compétences entrepreneuriales
    </a>
</div>
</%block>
<%block name="content">
<div class='panel panel-default page-block'>
    <div class='panel-body'>
        <div class='row'>
            <div class='col-xs-3' id='itemslist'>
            </div>
            <div class='col-xs-9' id='itemcontainer'>
                <div class='alert alert-info' style="margin: 30px 150px">
                    <h4>Sélectionner une compétence dans la liste à gauche</h4>
                </div>
            </div>
        </div>
        <div id='messageboxes'></div>
    </div>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
AppOptions['contexturl'] = "${contexturl}";
</%block>
