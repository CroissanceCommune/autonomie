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
<%inherit file="/admin/index.mako"></%inherit>
<%block name='content'>
    <h3 class='text-center'>Ajouter</h3>
    <hr>
    <div class='row'>
        <div class='col-md-6 col-md-offset-3'>
            <div class="alert alert-warning">
                <i class='fa fa-warning'></i>
                Les modèles de document doivent être au format odt pour pouvoir être utilisés par Autonomie
            </div>
            ${form|n}
        </div>
    </div>
</%block>
