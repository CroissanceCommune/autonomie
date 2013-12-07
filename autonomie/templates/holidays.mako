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
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="print_date" />
<%block name='content'>
<div class='row-fluid' style="padding-top:10px;">
    <div class='span6 offset3'>
        ${form|n}
        %if start_date and end_date:
            <h3>Congés entre le ${print_date(start_date)} et le ${print_date(end_date)}</h3>
        % endif
    </div>
</div>
<div class='row-fluid'>
    <div class='span6 offset3'>
        % if holidays:
        % for holiday in holidays:
            %if holiday.user:
                ${api.format_account(holiday.user)} : du ${print_date(max(holiday.start_date, start_date))} au ${print_date(min(holiday.end_date, end_date))}
                <br />
            % endif
        % endfor
    %else:
        Aucun congés n'a été déclaré sur cette période
    %endif
    </div>
</div>
</%block>
