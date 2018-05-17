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
<%block name="mainblock">
% if api.has_permission('edit.userdatas'):
    <div class="page-header-block">
        <button class="btn btn-primary primary-action" data-target="#step-forms" aria-expanded="true" aria-controls="step-forms" data-toggle="collapse">
            <i class="fa fa-plus"></i>
            Ajouter une étape
        </button>

        <div class='collapse' id="step-forms">
            <h4>Nouvelle étape de parcours</h4>
            <div class='col-md-12 col-lg-6'>
                <div class='container'>

                </div>
            </div>
        </div>
    </div>
% endif
<table class='table table-condensed'>
    <thead><tr><th>Date</th><th style="min-width:50%;">Etape</th><th>Echéance</th></tr></thead>
    <tbody>
        % if status_history:
        % for situation in status_history:
        <tr>
            <td>${api.format_date(situation.date)}</td>
            <td>${situation.situation.label}</td>
            <td>${api.format_date(situation.date)}</td>
        </tr>
        % endfor
        % else:
        <tr><td colspan=3>Le parcours de ce porteur de projet est vierge</td></tr>
        % endif
    </tbody>
</table>
</%block>
