<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
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
    <% keys = documents.keys() %>
    <% keys.sort() %>
    % for year in keys:
        <% subdirs = documents[year] %>
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
                    <th>Nom du fichier</th>
                    <th>Taille</th>
                    <th>Dernière consultation</th>
                    <th>Télécharger</th>
                </thead>
                <tbody>
            <% months = subdirs.keys() %>
            <% months.sort(key=lambda m:int(m)) %>
            % for month in months:
                <% files = subdirs[month] %>
                % for file_ in files:
                    <tr>
                        <td>${api.month_name(int(month))}</td>
                        <td>${file_.name}</td>
                        <td>${file_.size}</td>
                        <td>${api.format_date(file_.mod_date)}</td>
                        <td><a href="${file_.url(request)}">Télécharger&nbsp;<i class="fa fa-file-pdf-o fa-1x"></i></a></td>
                    </tr>
                % endfor
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
