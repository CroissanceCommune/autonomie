<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
  Display the documents of a given company
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
                    <i style="vertical-align:middle" class="icon-folder-open"></i>&nbsp;${year}
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
                    <th>Dernière modification</th>
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
                        <td><a href="${file_.url(request)}">Télécharger</a></td>
                    </tr>
                % endfor
            % endfor
                </tbody>
            </table>
        </div>
    % endfor
</div>
</%block>
