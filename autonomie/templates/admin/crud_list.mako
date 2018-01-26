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
<%doc>
:param str addurl: The url for adding items
:param str actions: List of actions buttons in the form [(url, label, icon, css, btn_type)]
:param list columns: The list of columns to display
:param list items: A list of dict {'id': <element id>, 'columns': (col1, col2), 'active': True/False}
:param obj stream_columns: A factory producing column entries [labels]
:param obj stream_actions: A factory producing action entries [(url, label, title, icon)]

:param str warn_msg: An optionnal warning message
:param str help_msg: An optionnal help message
</%doc>
<%inherit file="/admin/index.mako"></%inherit>
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%block name='afteradminmenu'>
<div class='page-header-block'>
    % if addurl is not UNDEFINED:
    <a class='btn btn-primary primary-action'
        href="${addurl}"
        title="Ajouter un élément à la liste"
    >
    <i class="fa fa-plus-circle"></i>&nbsp;Ajouter
    </a>
    % endif
    % if actions is not UNDEFINED:
        % for url, label, title, icon, css in actions:
            <a class="${css or 'btn btn-default'}"
                href="${url}"
                title="${title}"
                >
                <i class='${icon}'></i>&nbsp;${label}
            </a>
        % endfor
    % endif
    % if warn_msg is not UNDEFINED and warn_msg is not None:
    <div class="alert alert-danger">
        <i class='fa fa-warning'></i>
        ${warn_msg|n}
    </div>
    % endif
    % if help_msg is not UNDEFINED and help_msg is not None:
    <div class="alert alert-info">
        <i class='fa fa-help'></i>
        ${help_msg|n}
    </div>
    % endif
</div>
</%block>
<%block name='content'>
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
        % if widget is not UNDEFINED:
        ${request.layout_manager.render_panel(widget)}
        % endif
        <div class='page-block panel panel-default'>
            <div class='panel-body'>
                <table class='table table-stripped table-condensed'>
                <thead>
                % for column in columns:
                    <th>${column}</th>
                % endfor
                    <th style="text-align:right"> Actions </th>
                </thead>
                <tbody>
                % for item in items:
                    <tr
                        % if hasattr(item, 'active') and not item.active:
                            style="text-decoration: line-through;"
                        % endif
                        >
                        % for value in stream_columns(item):
                            <td>
                            % if value is not None:
                                ${ value|n }
                            % endif
                            </td>
                        % endfor
                        <td class='text-right'>
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
                                    % for action in stream_actions(item):
                                        <% url, label, title, icon = action[:4] %>
                                        % if len(action) >= 5:
                                        <% onclick = action[4] %>
                                        % else:
                                        <% onclick = None %>
                                        % endif
                                        ${dropdown_item(url, label, title, icon=icon, onclick=onclick)}
                                    % endfor
                                </ul>
                            </div>
                        </td>
                    </tr>
                % endfor
                % if not items:
                    <tr><td colspan='${len(columns) + 1}'>Aucun taux de tva n'a encore été configuré</td></tr>
                % endif
                </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
</%block>
