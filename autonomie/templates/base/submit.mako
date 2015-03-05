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
Submit buttons for special form renderings
</%doc>
<button type="${elem.type_}" name="${elem.name}" value="${elem.value}"
    title="${elem.title}"
% if elem.js:
    onclick="${elem.js}"
% endif
% if elem.css:
 class="${elem.css}"
% endif
>
% if elem.icon:
% if hasattr(elem.icon, "__iter__"):
% for icon in elem.icon:
    <i class="glyphicon glyphicon-${icon}"></i>
% endfor
% else:
    <i class='glyphicon glyphicon-${elem.icon}'></i>
% endif
% endif
${elem.label}
</button>
