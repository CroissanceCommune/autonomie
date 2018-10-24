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
<%block name='afteractionmenu'>
<div class='page-header-block'>
    <div class="pull-right btn-group" role='group'>
    ${request.layout_manager.render_panel('menu_dropdown', label="Exporter cette grille", links=export_btns)}
    </div>
    <div class='text-center'>
        <h4>
        Vos comptes de résultat pour l'année <b>${selected_year}</b>
        % if current_year != selected_year:
        <small>
        <a
            href="${request.route_path("/companies/{id}/accounting/income_statement_measure_grids", id=request.context.id)}"
            >
            Voir le compte de résultat de l'année courante
        </a>
        </small>
        % endif
        </h4>
    </div>
    <div class='text-center'>
    ${form|n}
    </div>
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    </div>
    <div class='panel-body'>
    % if not grid.is_void:
        <div class='table-responsive'>
        <table class='table table-bordered table-condensed'>
            <thead>
            % for header in grid.stream_headers():
            <th>${header}</th>
            % endfor
            </thead>
            <tbody>
            % for type_, row in grid.rows:
            <tr
            % if type_.is_total:
            class='highlighted'
            % endif
            >
            <td>${type_.label |n }</td>
                % for cell in row:
                <td>
                ${cell | n}
                </td>
                % endfor
            </tr>
            % endfor
            </tbody>
        </table>
        </div>
    % else:
        <h4>Aucun compte de résultat n'est disponible</h4>
    % endif
    </div>
</div>
</%block>
