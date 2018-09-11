<%doc>
 * Copyright (C) 2012-2018 Croissance Commune
 * Authors:
       * MICHEAU Paul <paul@kilya.biz>

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
        <% add_url = request.current_route_path(_query={'action': 'add_stage'}) %>
        <div class="page-header-block">
            <a class='btn btn-primary primary-action' href="${add_url}">
                <i class="glyphicon glyphicon-plus-sign"></i>&nbsp;Ajouter une étape de parcours
            </a>
        </div>
    % endif
    <table class='table table-condensed'>
        <thead><tr>
            <th>Date</th>
            <th>&Eacute;chéance</th>
            <th>&Eacute;tape</th>
            <th>Nouvelle situation</th>
            <th>&nbsp;</th>
        </tr></thead>
        <tbody>
            % if career_path:
                % for stage in career_path:
                    <% edit_url = request.route_path('career_path', id=stage.id, _query=dict(action='edit')) %>
                    <% del_url = request.route_path('career_path', id=stage.id, _query=dict(action='delete')) %>
                    <tr>
                        <td>${api.format_date(stage.start_date)}</td>
                        <td>${api.format_date(stage.end_date)}</td>
                        <td>
                            % if stage.career_stage is not None:
                                ${stage.career_stage.name}
                            % endif
                        </td>
                        <td class="text-muted">
                            % if stage.cae_situation is not None:
                                <small>${stage.cae_situation.label}</small>
                            % endif
                        </td>
                        <td class='text-right'>
                            <div class="btn-group">
                                <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                    Actions <span class="caret"></span>
                                </button>
                                <ul class="dropdown-menu dropdown-menu-right">
                                    <li><a href="${edit_url}"><i class="fa fa-pencil"></i>&nbsp;Voir/Modifier</a></li>
                                    <li>
                                        <a href="${del_url}" onclick="return confirm('Êtes vous sûr de vouloir supprimer cette étape de parcours ?')">
                                            <span class="text-danger"><i class="fa fa-remove"></i>&nbsp;Supprimer</span>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </td>
                    </tr>
                % endfor
            % else:
                <tr><td colspan=4 style="text-align:center; padding-top:20px; font-style:italic;">
                    Le parcours de ce porteur de projet est vierge
                </td></tr>
            % endif
        </tbody>
    </table>
</%block>
