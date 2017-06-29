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
<div role="tabpanel" class="tab-pane row" id="attached_files">
    <div class="col-md-10 col-md-offset-1 col-xs-12">
        <a class='btn btn-primary primary-action'
            href="${add_url}"
            title="Attacher un fichier">
            <i class='glyphicon glyphicon-plus-sign'></i>
            Attacher un fichier
        </a>
        <h3>${title}</h3>
        % for child in request.context.children:
            % if child.type_ == 'file':
                <div>
                    <dl class='dl-horizontal'>
                        <dt>Description du fichier</dt><dd>${child.description}</dd>
                        <dt>Taille du fichier</dt><dd>${api.human_readable_filesize(child.size)}</dd>
                        <dt>Dernière modification</dt><dd>${api.format_date(child.updated_at)}</dd>
                    </dl>
                        % if api.has_permission('edit.file', child):
                            <a class='btn btn-default btn-small'
                                href="${request.route_path('file', id=child.id)}">
                                <i class='glyphicon glyphicon-pencil'></i> Voir/modifier
                            </a>
                        % endif
                            <a class='btn btn-default btn-small'
                                href="${request.route_path('file', id=child.id, _query=dict(action='download'))}">
                                <i class='glyphicon glyphicon-download'></i> Télécharger
                            </a>
                        % if api.has_permission('edit.file', child):
                            <a class='btn btn-small btn-danger'
                                href="${request.route_path('file', id=child.id, _query=dict(action='delete'))}"
                                onclick="return confirm('Supprimer ce fichier ?');">
                                <i class='glyphicon glyphicon-trash'></i> Supprimer
                            </a>
                        % endif
                </div>
                <hr />
            % endif
        % endfor
    </div>
</div>
