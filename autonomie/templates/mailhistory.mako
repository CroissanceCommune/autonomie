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
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/pager.mako" import="pager"/>
<%block name='actionmenu'>
<div class='row'>
    <div class='col-md-12'>
        ${form|n}
    </div>
</div>
</%block>
<%block name="content">
<table class="table table-condensed">
    <thead>
        <tr>
            <th>Identifiant</th>
            <th>Entreprise</th>
            <th>Période</th>
            <th>Nom du fichier</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % for mail in records:
            <tr>
                <td>
                    ${mail.id}
                </td>
                <td>
                    ${mail.company.name}
                </td>
                <td>
                    ${api.month_name(int(mail.month))} ${mail.year}
                </td>
                <td>
                    ${mail.filename}
                </td>
                <td>
                Envoyé le ${api.format_datetime(mail.send_at)}
                </td>
                <td>
                    <a class='btn btn-success' href='${request.route_path("mail", id=mail.id)}'>Renvoyer</button>
                </td>
            </tr>
        % endfor
    </tbody>
</table>
${pager(records)}
</%block>
