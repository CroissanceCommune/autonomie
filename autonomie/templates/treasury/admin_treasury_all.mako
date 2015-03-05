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
<%inherit file="/base.mako"></%inherit>
<%block name='content'>
<div class='row'>
    <% keys = datas.keys() %>
    <% keys.sort() %>
    % for year in keys:
        <% months = datas[year] %>
        <div class='section-header'>
            <a href="#" data-toggle='collapse' data-target='#year_${year}'>
                <div>
                    <i style="vertical-align:middle" class="glyphicon glyphicon-folder-open"></i>&nbsp;${year}
                </div>
            </a>
        </div>
        % if year in current_years:
            <div class="section-content in collapse" id='year_${year}'>
        %else:
            <div class="section-content collapse" id='year_${year}'>
        %endif
            <table class="table table-striped table-bordered">
                <thead>
                    <th>Mois</th>
                    <th>Nombre de fichiers</th>
                    <th>Actions</th>
                </thead>
                <tbody>
                <% month_names = months.keys() %>
                <% month_names.sort(key=lambda m:int(m)) %>
                % for month in month_names:
                    <% month_datas = months[month] %>
                    <tr>
                        <td>${month_datas['label']}</td>
                        <td>${month_datas['nbfiles']} fichier(s)</td>
                        <td><a href="${month_datas['url']}">Administrer</a></td>
                    </tr>
                % endfor
            % if not months:
                <tr><td colspan='5'>Aucun document n'est disponible</td></tr>
            % endif
                </tbody>
            </table>
        </div>
    % endfor
    % if not keys:
        <div>Aucun document n'est disponible</div>
    % endif
</div>
</%block>
