# -*- coding: utf-8 -*-
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

# -*- coding: utf-8 -*-
%if field.schema.css_class:
    <div class="${field.schema.css_class}">
%else:
    <div>
% endif
    ${field.serialize(cstruct)|n}
% if field.error and not field.widget.hidden and not field.typ.__class__.__name__ == 'Mapping':
    <br />
    %for msg in field.error.messages():
        <p class="${field.widget.error_class}">${msg}</p>
    %endfor
% endif
</div>
