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
            ${item.render(request)|n}
            <li class='divider-vertical'>
        % endfor
    </ul>
% endif

