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
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
        <a href="${request.route_path('userdatas', _query=dict(action='new'))}">
            Nouvelle entrée gestion sociale
        </a>
    </li>
    % if api.has_permission('admin'):
    <li>
        <a href="${request.route_path('import_step1')}">
            Importer des données
        </a>
        </li>
    % endif
</ul>
<div class='row'>
    <div class='col-md-8'>
        <div class='row'>
            ${form|n}
        </div>
    </div>
    <div class='col-md-4'>
        <div class='well well-sm pull-right btn-group' role='group'>
            <%
        args = request.GET
        url = request.route_path('userdatas.xls', _query=args)
        %>
        <a
            class='btn btn-default'
            href='${url}'
            title="Exporter les éléments de la liste au format xls">
            <i class='fa fa-file-excel-o'></i>&nbsp;Excel
        </a>
            <%
        args = request.GET
        url = request.route_path('userdatas.ods', _query=args)
        %>
        <a
            class='btn btn-default'
            href='${url}'
            title="Exporter les éléments de la liste au format ods">
            <i class='fa fa-file'></i>&nbsp;ODS
        </a>
            <%
        args = request.GET
        url = request.route_path('userdatas.csv', _query=args)
        %>
        <a
            class='btn btn-default'
            href='${url}'
            title="Exporter les éléments de la liste au format csv">
            <i class='fa fa-file'></i>&nbsp;CSV
        </a>
        </div>
    </div>
</div>
</%block>
<%block name="content">
<table class="table table-condensed table-hover">
    <thead>
        <tr>
            <th>${sortable("Nom", "lastname")}</th>
            <th>Accompagnateur</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % for userdata in records:
            <% url = request.route_path('userdata', id=userdata.id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <% css = "white_" %>
            <tr class='${css}tr'>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(userdata)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(userdata.situation_follower)}
                </td>
                <td class="actions">
                        <% edit_url = request.route_path('userdata', id=userdata.id) %>
                        ${table_btn(edit_url, u"Voir/éditer", u"Voir / Éditer", icon='glyphicon glyphicon-pencil')}
                    % if api.has_permission('delete', userdata):
                        <% del_url = request.route_path('userdata', id=userdata.id, _query=dict(action="delete")) %>
<% del_msg = u'Êtes vous sûr de vouloir supprimer les données de cette personne ?'
if userdata.user is not None:
    del_msg += u' Le compte associé sera également supprimé.'
    del_msg += u" Cette action n'est pas réversible."
%>
                        ${table_btn(del_url, \
                        u"Supprimer",  \
                        u"Supprimer cette entrée", \
                        icon='glyphicon glyphicon-trash', \
                        onclick=u"return confirm(\"%s\");" % del_msg,\
                        css_class="btn-danger")
                        }
                    % endif
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
