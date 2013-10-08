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

<div class="deformFileupload">

  <input type="hidden" name="__start__" value="${field.name}:mapping"/>

    <input type="file" name="upload" class="${field.widget.css_class}" size="${field.widget.size}"  id="${field.oid}"/>
    %if cstruct.get('uid'):
      <div class="deformReplaces">
        <input type="hidden" name="uid" value="${cstruct['uid']}"
           id="${field.oid}-uid"/>
      </div>
        % if cstruct.get('preview_url'):
            <span class="help-block">
                <a href='${cstruct['preview_url']}'>${cstruct.get('filename')}</a>
            </span>
        % endif
    % endif
    <input type="hidden" name="__end__" value="${field.name}:mapping"/>
</div>

