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
<%namespace file="autonomie:templates/base/utils.mako" import="format_text" />
<%block name="content">
<a class='btn btn-default pull-right hidden-print' href='#print' onclick="window.print()">
    <i class='glyphicon glyphicon-print'></i>Imprimer
</a>
<div class='row' style="margin-bottom: 40px">
    <div class="col-xs-12">
        <h1 class='text-center'>${title}</h1>
        <div>
            <b>Nom Prénom :&nbsp;${request.context.contractor.label}</b>
        </div>
    </div>
</div>
<div class='row'>
    <div class='col-xs-12'>
        <table class='table table-bordered'>
            <tr>
            % for grid in grids:
                <td>Date d'auto évaluation ${grid.deadline.label} : ${api.format_date(grid.updated_at)}</td>
            % endfor
            </tr>
        </table>
    </div>
</div>
<div class='row' style='page-break-after:always;'>
    <div class='col-xs-12'>
        <b>Référent </b>: ${api.format_account(request.context.contractor.userdatas.situation_follower)}
    </div>
</div>
<div class='row'>
    <div class='col-xs-12'>
        <h2 class='text-center'>Cartographie des compétences auto-évaluées</h2>
    </div>
</div>
<div class='row'>
    <div class='col-xs-8 col-offset-xs-2' id='radar' style='page-break-after:always;'>
    </div>
</div>
<div class='row'>
    <div class='col-xs-12'>
        <h2 class='text-center'>Grille d'autonomie</h2>
        <h3 class='text-center' style='margin-bottom: 30px'>
            Auto-évaluation et évolution des compétences entrepreneuriales
        </h3>

        % for item in grids[0].items:
            <% option = item.option %>
            <div class='panel panel-default' style='page-break-after:always;'>
                <div class='panel-heading'>
                    <h3>${option.label}</h3>
                </div>
                    <table class='table table-stripped table-condensed table-bordered'>
                    <thead>
                        <tr>
                            <th style='width: 30%'></th>
                            % for deadline in deadlines:
                                <th
                                    % if not loop.last:
                                    colspan='${len(scales)}'
                                    % else:
                                    colspan='${len(scales) + 1}'
                                    % endif
                                    >
                                    Évaluation ${deadline.label}
                                </th>
                                % if not loop.last:
                                    <th></th>
                                % endif
                            % endfor
                        </tr>
                        <tr>
                            <th>Compétences entrepreneuriales</th>
                            % for deadline in deadlines:
                                % for scale in scales:
                                    <th>
                                        ${scale.label}
                                    </th>
                                % endfor
                                % if not loop.last:
                                    <th></th>
                                % endif
                            % endfor
                            <th>Argumentaires/preuves</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for suboption in option.children:
                            <tr>
                                <td>${suboption.label}</td>
                                % for grid in grids:
                                    <% grid_subitem = grid.ensure_item(option).ensure_subitem(suboption) %>
                                    % for scale in scales:
                                        <td style='min-width:15px'>
                                            % if grid_subitem.scale.id == scale.id:
                                                <div class='text-center'
                                                style="background-color: #545454;with:100%;height:100%;"
                                            >
                                            <i class='fa fa-check'></i>
                                            % endif
                                        </div>
                                        </td>
                                    % endfor
                                    <td>
                                        % if loop.last:
                                            ${format_text(grid_subitem.comments)}
                                        % endif
                                    </td>
                                % endfor
                            </tr>
                        % endfor
                    </tbody>
                </table>
        </div>
        % endfor
    </div>
</div>
<div class='row'>
    <div class='col-xs-12'>
        <h2 class='text-center'>Axe de progrès identifiés</h2>
        <table class='table table-stripped table-condensed table-bordered'>
            <thead>
                <th>Compétences</th>
                <th>Axe de progrès</th>
            </thead>
            <tbody>
                % for item in grids[-1].items:
                    <tr>
                        <td style='width: 30%'>${item.option.label}</td>
                        <td>${format_text(item.progress)}</td>
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
</%block>
