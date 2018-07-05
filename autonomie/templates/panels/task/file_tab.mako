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
<%def name="showfile(file_object)">
<div>
    <dl class='dl-horizontal'>
        <dt>Description du fichier</dt><dd>${file_object.description}</dd>
        <dt>Taille du fichier</dt><dd>${api.human_readable_filesize(file_object.size)}</dd>
        <dt>Dernière modification</dt><dd>${api.format_date(file_object.updated_at)}</dd>
    </dl>
    ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(request, file_object))}
</div>
</%def>
<div role="tabpanel" class="tab-pane row" id="attached_files">
    <div class="col-xs-12">
        <button class='btn btn-primary primary-action'
            onclick="window.openPopup('${add_url}')"
            title="Attacher un fichier">
            <i class='glyphicon glyphicon-plus-sign'></i>
            Attacher un fichier
        </button>
        <h3>${title}</h3>
        % for file_object in files:
            <div class='row'>
                <div class='col-xs-12'>
                <dl class='dl-horizontal'>
                    <dt>Description du fichier</dt><dd>${file_object.description}</dd>
                    <dt>Taille du fichier</dt><dd>${api.human_readable_filesize(file_object.size)}</dd>
                    <dt>Dernière modification</dt><dd>${api.format_date(file_object.updated_at)}</dd>
                </dl>
                    ${request.layout_manager.render_panel('menu_dropdown', label="Actions", links=stream_actions(request, file_object))}
                </div>
            </div>
            <hr />
        % endfor
    </div>
</div>
