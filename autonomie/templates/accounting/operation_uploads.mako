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
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<a class="btn btn-default large-btn
    % if '__formid__' in request.GET:
        btn-primary
    % endif
    " href='#filter-form' data-toggle='collapse' aria-expanded="false" aria-controls="filter-form">
    <i class='glyphicon glyphicon-filter'></i>&nbsp;
    Filtres&nbsp;
    <i class='glyphicon glyphicon-chevron-down'></i>
</a>
% if '__formid__' in request.GET:
    <span class='help-text'>
        <small><i>Des filtres sont actifs</i></small>
    </span>
    <div class='help-text'>
        <a href="${request.current_route_path(_query={})}">
            <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
        </a>
    </div>
% endif
% if '__formid__' in request.GET:
    <div class='collapse' id='filter-form'>
% else:
    <div class='in collapse' id='filter-form'>
% endif
        <div class='row'>
            <div class='col-xs-12'>
<hr/>
                ${form|n}
            </div>
        </div>
<hr/>
    </div>
<table class="table table-striped table-condensed table-hover">
    <thead>
        <tr>
            <th class="visible-lg">${sortable(u"Traité le", "created_at")}</th>
            <th class="visible-lg">${sortable(u"Date", "date")}</th>
            <th>${sortable(u"Nom du fichier", "filename")}</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for entry in records:
                <tr class='tableelement' id='${entry.id}'>
                    <td>${api.format_datetime(entry.created_at)}</td>
                    <td>${api.format_date(entry.date)}</td>
                    <td>
                        ${entry.filename}
                    </td>
                    <td class='actions'>
                        <div class='btn-group'>
                            <button
                                type="button"
                                class="btn btn-default dropdown-toggle"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">
                                Actions <span class="caret"></span>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-right">
                                % for url, label, title, icon, options in stream_actions(entry):
                                    ${dropdown_item(url, label, title, icon=icon, **options)}
                                % endfor
                            </ul>
                        </div>
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='4'>
                    Aucun fichier n'a été traité
                </td>
            </tr>
    % endif
${pager(records)}
</%block>
