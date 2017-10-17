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
<%block name='afteractionmenu'>
<div class='page-header-block'>
% if current_grid is not None:
    <div class='text-center'>
        <h4>
        Votre
        trésorerie au <b>${api.format_date(current_grid['date'])}</b>
        % if last_grid != current_grid:
        <small>
        <a
            href="${request.route_path("/companies/{id}/accounting/treasury_measure_grids", id=request.context.company.id)}"
            >
            Voir le dernier état de trésorerie
        </a>
        </small>
        % endif
        </h4>
    </div>
    <% measures = current_grid['measures'] %>
    <div class='row'>
        <div class='col-xs-12 col-md-3 col-lg-3 text-center'>
            ## 1 est un internal_id defini par le cdc de ce module
            % if 1 in measures:
                <h4>${measures[1][0]['label'] | n}</h4>
            <div class='primary-text-lg'>
                ${api.format_amount(measures[1][0]['value'], precision=0) | n}&nbsp;€
            </div>
            % endif
        </div>
        <div class='col-xs-12 col-md-6'>
            <% keys = measures.keys() %>
            <% keys.sort() %>
            <table class='table table-striped table-condensed' style="font-size: 14px">
            % for key in keys:
                % for measure in measures[key]:
                <tr >
                    <td style="vertical-align:middle">
                    % if key in (1, 4, 8):
                    <h3>
                    % endif
                    ${measure['label'] | n}
                    % if key in (1, 4, 8):
                    </h3>
                    % endif
                    </td>
                    <td class='text-right'>
                    <h4>
                    ${api.format_amount(measure['value'], precision=0)|n}&nbsp;€
                    </h4>
                    </td>
                </tr>
                % endfor
            % endfor
            </table>
        </div>
    </div>
% else:
<h4>Aucun état de trésorerie n'est disponible</h4>
% endif
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
<div class='panel-heading'>
<h3>Historique des états trésorerie</h3>
<a  href='#filter-form' data-toggle='collapse' aria-expanded="false" aria-controls="filter-form">
    <i class='glyphicon glyphicon-search'></i>&nbsp;
    Filtres&nbsp;
    <i class='glyphicon glyphicon-chevron-down'></i>
</a>
% if '__formid__' in request.GET:
    <div class='help-text'>
        <small><i>Des filtres sont actifs</i></small>
    </div>
    <div class='help-text'>
        <a href="${request.current_route_path(_query={})}">
            <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
        </a>
    </div>
% endif
</div>
<div class='panel-body'>
    <div class='collapse' id='filter-form'>
        <div class='row'>
            <div class='col-xs-12'>
                ${form|n}
            </div>
        </div>
    </div>
</div>
</div>
% if records is not None:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    ${records.item_count} Résultat(s)
    </div>
    <div class='panel-body'>
        <table class="table table-striped table-condensed table-hover">
            <thead>
                <tr>
                    <th class="visible-lg">${sortable(u"Date", "date")}</th>
                    <th class="visible-lg">Trésorerie du jour</th>
                    <th class="actions">Actions</th>
                </tr>
            </thead>
            <tbody>
                % if records:
                    % for record in records:
                        <tr
                        % if record.id == current_grid['id']:
                        class="tr_highlighted"
                        % endif
                        >
                            <% url = request.route_path("/treasury_measure_grids/{id}", id=record.id) %>
                            <% onclick = "document.location='{url}'".format(url=url) %>
                            <td onclick="${onclick}" class="visible-lg rowlink" >
                                ${api.format_date(record.date)}
                            </td>
                            <td onclick="${onclick}" class="visible-lg rowlink" >
                                ${api.format_amount(record.get_first_measure().value, precision=0)|n}&nbsp;€
                            </td>
                            <td class="actions">
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
                                        % for url, label, title, icon, options in stream_actions(record):
                                            ${dropdown_item(url, label, title, icon=icon, **options)}
                                        % endfor
                                    </ul>
                                </div>
                            </td>
                        </tr>
                    % endfor
                % else:
                    <tr>
                        <td colspan='6'>
                            Aucun client n'a été référencé
                        </td>
                    </tr>
                % endif
            </tbody>
        </table>
        ${pager(records)}
    </div>
</div>
% endif
</%block>
