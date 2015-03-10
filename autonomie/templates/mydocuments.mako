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
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_filetable" />
<%namespace file="/base/utils.mako" import="table_btn" />
<%block name='content'>
<div class="row" style="margin-top:10px">
    <div class="col-md-12">
        <span class='help-block'>
            <i class='fa fa-question-circle fa-2x'></i>
            Retrouvez ici l'ensemble des documents sociaux ayant été associés à votre compte dans Autonomie.
        </span>
        <h3>Documents déposés dans Autonomie</h3>
        ${format_filetable(documents)}
        <h3>Documents sociaux téléchargeables</h3>
        <table class="table table-striped table-bordered table-hover">
            <thead>
                <th>Description</th>
                <th>Nom du fichier</th>
                <th>Déposé le</th>
                <th class="actions">Actions</th>
            </thead>
            <tbody>
                <% loaded = [] %>
                % for document in generated_docs:
                    % if not document.template_id in loaded:
                        <% url = request.route_path( \
                        'userdata', \
                        id=document.userdatas_id, \
                        _query=dict(template_id=document.template_id, \
                        action="py3o")) %>
                        <tr>
                            <td>${document.template.description}</td>
                            <td>${document.template.name}</td>
                          <td>
                              ${api.format_date(document.created_at)}
                          </td>
                            <td class="actions">
                                ${table_btn(url,
                               u"Télécharger",
                               u"Télécharger ce document",
                               icon="download-alt")}
                            </td>
                        </tr>
                        <% loaded.append(document.template_id) %>
                    % endif
                % endfor
            </tbody>
        </table>
    </div>
</div>
</%block>
