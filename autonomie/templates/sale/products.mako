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
<%inherit file="/base.mako"></%inherit>
<%block name="content">
<div class='row'>
    <div class='col-xs-3' id='category_list'>
    </div>
    <div class='col-xs-9' id='product_container'>
            <div class='alert alert-info' style="margin: 30px 150px">
                % if not request.context.products:
                    <h4>Configuration du catalogue produit</h4>
                    <ul>
                        <li>1 - Ajouter une catégorie de produits</li>
                        <li>2 - Ajouter des produits</li>
                        <li>3 - Ajouter des ouvrages</li>
                    </ul>
                    % else:
                        <h4>Sélectionner une catégorie dans la liste à gauche</h4>
                % endif
            </div>
    </div>
</div>
<div id='popup_container'>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
AppOptions['contexturl'] = "${contexturl}";
</%block>
