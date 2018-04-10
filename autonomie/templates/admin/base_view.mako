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

<%doc>
    Admin common page template
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_text"/>
<%block name="afteradminmenu">
% if not message is UNDEFINED and message:
    <div class='alert alert-info'>
        ${format_text(message)}
    </div>
% endif
</%block>
<%block name='content'>
% if  not form is UNDEFINED:
<div class='row'>
    <div class="col-md-10 col-md-offset-1">
        <div class='page-block panel panel-default'>
            % if not form is UNDEFINED:
                ${form|n}
            % endif
        </div>
    </div>
</div>
% endif
</%block>
