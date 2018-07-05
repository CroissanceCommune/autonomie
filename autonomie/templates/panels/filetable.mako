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
% if help_message is not UNDEFINED and help_message is not None:
<div class='alert alert-info'>
    <i class='fa fa-question-circle fa-2x'></i>
    ${help_message | n}
</div>
% endif
% if request.has_permission(add_perm):
<button
    class='btn btn-primary primary-action'
    onclick='openPopup("${add_url}");'
    title="Déposer un document dans autonomie"
    >
    <i class="glyphicon glyphicon-plus"></i>
    Déposer un document
</button>
% endif
<table class="table table-striped table-hover">
    <thead>
        <th>Document parent</th>
        <th>Type de document</th>
        <th>Nom du fichier</th>
        <th>Déposé le</th>
        <th class="actions">Actions</th>
    </thead>
    <tbody>
    % for doc in files:
        <tr>
            <td>${parent_label(doc)}</td>
            <td>
            % if doc.file_type_id:
            ${doc.file_type.label}
            % endif
            <td>${doc.name}</td>
            <td>${api.format_date(doc.updated_at)}</td>
            <td class='text-right'>
            ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(request, doc))}
            </td>
          </tr>
    % endfor
    % if documents == []:
        <tr><td colspan='6'>Aucun document n'est disponible</td></tr>
    % endif
    </tbody>
</table>
