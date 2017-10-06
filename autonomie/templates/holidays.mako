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

<%doc>
Template for holidays search
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%block name='content'>
<div class='row' style="padding-top:10px;">
    <div class='col-md-6 col-md-offset-3'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Recherche
    </div>
    <div class='panel-body'>
                ${form|n}
            </div>
        </div>
    </div>
</div>
%if start_date and end_date:
<div class='row'>
    <div class='col-md-6 col-md-offset-3'>
        <div class='panel panel-default page-block'>
            <div class='panel-heading'>
                    Congés entre le ${api.format_date(start_date)} et le ${api.format_date(end_date)} :
            ${holidays.count()} Résultat(s)
            </div>
            <div class='panel-body'>
                % if holidays:
                <table class='table table-stripped table-condensed'>
                    <thead>
                    <th>Nom</th>
                    <th>Date de début</th>
                    <th>Date de fin</th>
                    </thead>
                    <tbody>
                    % for holiday in holidays:
                        %if holiday.user:
                        <tr>
                        <td>
                            ${api.format_account(holiday.user)}
                        </td>
                        <td>
                        ${api.format_date(max(holiday.start_date, start_date))}
                        </td>
                        <td>
                        ${api.format_date(min(holiday.end_date, end_date))}
                        </td>
                        </tr>
                        % endif
                    % endfor
                %else:
                <tr><td colspan='3'>
                    Aucun congés n'a été déclaré sur cette période
                    </td>
                    </tr>
                %endif
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
% endif
</%block>
