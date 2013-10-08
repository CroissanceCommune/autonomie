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
<%doc>
Select for tva amount
</%doc>
<select name="${field.name}" id="${field.oid}"
% if hasattr(field.widget, "css_class"):
class="${field.widget.css_class}"
% endif
>
% for value, description in values:
<option
%if value == cstruct:
selected="selected"
% endif
 value="${value}">${description}</option>
% endfor
</select>
% if field.name == 'tva':
<script>
 deform.addCallback(
    "${field.oid}",
    function (oid) {
      $('#' + oid + " select").change(function(){
          onTvaSelect(this);
          var row = $(this).parent().parent();
          $(Facade).trigger("linechange", row);
          $(Facade).trigger("totalchange", row);
      })
    });
</script>
% endif
