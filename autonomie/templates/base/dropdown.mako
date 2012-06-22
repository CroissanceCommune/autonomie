<%doc>
Dropdown menu template
</%doc>
% if elem.permitted(request.context, request):
<li class='dropdown'>
<a class='dropdown-toggle' data-toggle='dropdown' href='#'>
    ${elem.label}
<b class="caret"></b>
</a>
<ul class='dropdown-menu'>
% for subitem in elem.items:
    ${subitem.render(request)|n}
% endfor
</ul>
</li>
% endif
