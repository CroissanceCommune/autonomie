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
    Template used to render action buttons (see utils/widgets.py)
    item is the current item the action is made on
    elem is the current link object
</%doc>
% if elem.permitted(item, request):
    <a title='${elem.title}' href="${elem.url(item, request)}"
      %if elem.onclick():
          onclick="${elem.onclick()}"
      %endif
% if elem.css:
    class="${elem.css}"
       % endif
      >
      %if elem.icon:
        %if hasattr(elem.icon, "__iter__"):
            %for icon in elem.icon:
                <i class="${icon}"></i>
            % endfor
        %else:
          <i class='${elem.icon}'></i>
        % endif
      % endif
      <span class="visible-desktop hidden-tablet" style="display:inline">
      ${elem.label}
      </span>
    </a>
% endif
