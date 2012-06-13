<%doc>
Render an action menu
</%doc>
% if elem.items:
    <ul class='nav nav-pills'>
    % for item in elem.items:
        % if hasattr(item, "selected") and item.selected(request):
            <li class='active'>
        % else:
            <li>
        % endif
        ${item.render(request)|n}
        </li>
    % endfor
    </ul>
% endif
