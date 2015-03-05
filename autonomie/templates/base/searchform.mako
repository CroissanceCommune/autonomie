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
Template used to render a search form
</%doc>
<% from autonomie.views.forms.lists import ITEMS_PER_PAGE_OPTIONS %>
<form class='navbar-form col-md-offset-1 pull-right form-search form-inline' id='${elem.id_}' method='GET'>
    <div class='pull-left'>
        <input type='text' name='search' class='input-medium search-query' value="${elem.defaults['search']}">
        % if elem.helptext:
            <span class="help-block">${elem.helptext}</span>
        %endif
    </div>
    <select name='items_per_page'>
        % for text, value in ITEMS_PER_PAGE_OPTIONS:
            % if int(value) == int(elem.defaults['items_per_page']):
                <option value="${value}" selected='true'>${text}</option>
            %else:
                <option value="${value}">${text}</option>
            %endif
        % endfor
    </select>
    <button type="submit" class="btn btn-default" class='vertical-align:bottom;'>${elem.submit_text}</button>
</form>
