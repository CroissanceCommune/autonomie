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
<%namespace file="/base/utils.mako" import="format_filetable" />
<%block name="mainblock">
% if request.has_permission('add.file'):
<div class='alert alert-info'>
    <i class='fa fa-question-circle fa-2x'></i>
    Cette liste présente l'ensemble des documents déposés rattachés à cette affaire ou aux documents (devis/factures) qui lui sont associées<br />
    <br />
    <br />
    <a class='btn btn-success'
    href="${request.route_path('/businesses/{id}', id=current_business.id, _query=dict(action='attach_file'))}"
    title="Rattacher un document à cette affaire">
    <i class="glyphicon glyphicon-plus"></i>
    Déposer un document
</a>
</div>
% endif
${format_filetable(current_business.children)}
</%block>
