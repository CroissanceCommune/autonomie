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
<%inherit file="${context['main_template'].uri}" />
<%block name='afteractionmenu'>
<div class='row page-header-block'>
    % if navigation and not request.is_popup:
    <ul class="breadcrumb breadcrumb-arrow">
        <li><a href='${navigation.url}'><i class='fa fa-chevron-left'></i></a></li>
        <li>
        <a href="${navigation.url}">${navigation.title}</a>
        </li>
    </ul>
    % endif
    <div class='page-header-block'>
    <a
        class='btn btn-primary primary-action'
        href="${download_url}"
        >
        <i class='fa fa-download'></i>&nbsp;Télécharger ce fichier
    </a>
    % if request.has_permission('edit.file', file):
    <a
        class='btn btn-default secondary-action'
        href="${edit_url}"
    >
    <i class='fa fa-pencil'></i>&nbsp;Modifier ce fichier
    </a>
    % endif
    % if request.has_permission('delete.file', file):
    <a
        class='btn btn-danger secondary-action'
        href="${delete_url}"
        onclick="return confirm('Êtes-vous sûr de vouloir supprimer ce fichier ?')"
    >
    <i class='fa fa-trash'></i>&nbsp;Supprimer définitivement ce fichier
    </a>
    % endif
    </div>
</div>
</%block>
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-body'>
        <div class='row'>
            <div class='col-md-6 col-md-offset-3'>
                <dl class='dl-horizontal'>
                    <dt>Description du fichier</dt><dd>${file.description}</dd>
                    <dt>Nom du fichier</dt><dd> ${file.name}</dd>
                    <dt>Taille du fichier</dt><dd>${api.human_readable_filesize(file.size)}</dd>
                    <dt>Date de dépôt</dt><dd>${api.format_date(file.created_at)}</dd>
                    <dt>Dernière modification</dt><dd>${api.format_date(file.updated_at)}</dd>
                </dl>
            </div>
        </div>
    </div>
</div>
</%block>
