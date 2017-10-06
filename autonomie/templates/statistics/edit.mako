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
<%block name='afteractionmenu'>
    <div class="alert alert-info">
        <i class='fa fa-help'></i>
        Configurez la feuille de statistiques ${request.context.title} :
        <ul>
            <li>Ajouter des entrées statistiques</li>
            <li>Composer vos entrées statistiques à l'aide de un ou plusieurs critères</li>
        </ul>
        Vous pouvez alors
        <ul>
            <li>Générer le fichier tableur pour cette feuille de statistiques</li>
            <li>Pour chaque entrée statistique, exporter l'ensemble des entrées de gestion sociale correspondantes</li>
        </ul>
    </div>
</%block>
<%block name="content">
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
        <div id='sheet'>
        </div>
    </div>
    <div class='panel-body'>
        <div class='row' style="margin-bottom: 30px">
            <div class='col-xs-12' id='entrylist'>
            </div>
        </div>
        <div class='row' style="margin-top: 30px;">
            <div id='entry_edit' class='col-xs-10 col-xs-offset-1' ></div>
        </div>
    </div>
</div>
<div id='messageboxes'></div>
<div id='popup_container'></div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
AppOptions['contexturl'] = "${contexturl}";
</%block>
