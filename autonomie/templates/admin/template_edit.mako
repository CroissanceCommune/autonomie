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
<%inherit file="/admin/index.mako"></%inherit>
<%block name='content'>
<div class='row'>
    <div class='col-md-6 col-md-offset-3 well'>
        <dl class='dl-horizontal'>
            <dt>Description du fichier</dt><dd>${request.context.description}</dd>
            <dt>Nom du fichier</dt><dd> ${request.context.name}</dd>
            <dt>Taille du fichier</dt><dd>${api.human_readable_filesize(request.context.size)}</dd>
            <dt>Date de dépôt</dt><dd>${api.format_date(request.context.created_at)}</dd>
            <dt>Dernière modification</dt><dd>${api.format_date(request.context.updated_at)}</dd>
            <dt></dt>
            <dd><a class='' href="${request.route_path('file', id=request.context.id, _query=dict(action='download'))}">Télécharger le fichier</a></dd>
        </dl>
        <a href="${request.route_path('template', id=request.context.id, _query=dict(action='delete'))}"
           onclick="return confirm('Êtes-vous sûr de vouloir supprimer ce document ?');"
           >
           <i class='glyphicon glyphicon-trash'></i>Supprimer
       </a>
    </div>
</div>
<h3 class='text-center'>Éditer</h3>
<hr>
<div class='row'>
    <div class='col-md-6 col-md-offset-3'>
        ${form|n}
    </div>
</div>
</%block>
