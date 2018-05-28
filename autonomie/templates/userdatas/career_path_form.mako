<%doc>
 * Copyright (C) 2012-2018 Croissance Commune
 * Authors:
       * MICHEAU Paul <paul@kilya.biz>

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
    Career path form rendering
</%doc>

<%inherit file="${context['main_template'].uri}" />

<%block name="mainblock">
    ${request.layout_manager.render_panel(
        'help_message_panel', 
        parent_tmpl_dict=context.kwargs
    )}
    <div class="col-md-10 col-md-offset-1">
        <div class='panel panel-default page-block'>
            <div class='panel-body'>
                ${form|n}
            </div>
        </div>
    </div>
</%block>
