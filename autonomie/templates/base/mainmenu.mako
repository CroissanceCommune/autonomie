<%doc>
    Main menu widget
</%doc>
% if elem.items:
    <ul
        % if hasattr(elem, "css"):
            class="nav ${elem.css}">
        % else:
            class='nav'>
        % endif
        % for item in elem.items:
            % if item.permitted(request.context, request):
                ${item.render(request)|n}
                <li class='divider-vertical'></li>
            % endif
        % endfor
    </ul>
% endif

