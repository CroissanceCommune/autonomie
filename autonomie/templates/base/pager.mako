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
