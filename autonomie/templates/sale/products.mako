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
<%block name="content">
<div class='row'>
    <div class='col-xs-2' id='category_list'>
    </div>
    <div class='col-xs-9 col-xs-offset-1' id='product_container'>
            <div class='alert alert-info' style="margin: 30px 150px 30px 50px">
                % if not request.context.sale_catalog:
                    Le catalogue produit permet de configurer des produits et des ouvrages en les rangeant par catégories.
                    <br />
                    Lors de l'insertion de ces éléments dans un devis ou une
                    facture, les champs configurés seront utilisés pour
                    pré-remplir le document.
                    <br />
                    <br />
                    <h4>Configuration du catalogue produit</h4>
                    <ul>
                        <li>1 - Ajouter une catégorie</li>
                        <li>2 - Ajouter des produits</li>
                        <li>3 - Ajouter des ouvrages (groupe de produits)</li>
                    </ul>
                    <br />
                    <a class="btn btn-success" href="#categories/add" title="Ajouter une catégorie">Commencer par ajouter une catégorie</a>
                    % else:
                        <h4>Sélectionner une catégorie dans la liste à gauche</h4>
                % endif
            </div>
    </div>
</div>
<div id='messageboxes'></div>
<div id='popup_container'>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
AppOptions['contexturl'] = "${contexturl}";
AppOptions['all_products_url'] = "${all_products_url}";
</%block>
