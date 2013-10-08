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
pager template
</%doc>
<%namespace file='/base/utils.mako' import='urlbuild' />
<%def name="pager(items)">
<div class="pager">
  <% link_attr={"class": "btn small"} %>
  <% curpage_attr={"class": "btn primary small disabled"} %>
  <% dotdot_attr={"class": "btn small disabled"} %>

  ${items.pager(format="$link_previous ~2~ $link_next",
  link_attr=link_attr,
  curpage_attr=curpage_attr,
  dotdot_attr=dotdot_attr)}
</div>
</%def>
<%def name="sortable(label, column)">
<% sort_column = request.GET.get("sort", "") %>
<% sort_direction = request.GET.get("direction", "asc") %>
%if (column == sort_column):
  <% css_class = "current " + sort_direction %>
%else:
  <% css_class = ""%>
%endif
%if sort_direction == "asc":
  <% direction = "desc" %>
%else:
  <% direction = "asc"%>
%endif
<% args_dict = dict(direction=direction, sort=column) %>

<a href="${api.urlupdate(request, args_dict)}" class='${css_class}'>
    %if direction =='asc':
        <i class="icon-chevron-up"></i>
    %else:
        <i class="icon-chevron-down"></i>
    %endif
  ${label}
  </a>
</%def>
