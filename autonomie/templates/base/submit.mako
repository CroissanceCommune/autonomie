<%doc>
Submit buttons for special form renderings
</%doc>
% if elem.permitted(request.context, request):
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
 <i class="${icon}"></i>
% endfor
% else:
 <i class='${elem.icon}'></i>
% endif
% endif
${elem.label}
</button>
% endif
