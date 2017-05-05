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
:param str addurl: The url to the add form
:param list columns: The list of columns to display
:param list items: A list of dict {'id': <element id>, 'columns': (col1, col2), 'active': True/False}
:param obj stream_columns: A factory producing column entries [labels]
:param obj stream_actions: A factory producing action entries [(url, label, icon, btn_type)]
                           btn_type is one of the known btn classes

:param str warn_msg: An optionnal warning message
:param str help_msg: An optionnal help message
</%doc>
<%inherit file="/admin/index.mako"></%inherit>
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%block name='content'>
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
    <div class='well'>
        <a class='btn btn-success'
            href="${addurl}"
            title="Ajouter un élément à la liste"
        >
        Ajouter
    </a>
    </div>
    % if warn_msg is not UNDEFINED and warn_msg is not None:
        <div class="alert alert-danger">
            <i class='fa fa-warning'></i>
            ${warn_msg}
        </div>
    % endif
    % if help_msg is not UNDEFINED and help_msg is not None:
        <div class="alert alert-info">
            <i class='fa fa-help'></i>
            ${help_msg}
        </div>
    % endif
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
                <td>${ value|n }</td>
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
                        % for url, label, title, icon in stream_actions(item):
                            ${dropdown_item(url, label, title, icon=icon)}
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
</%block>
