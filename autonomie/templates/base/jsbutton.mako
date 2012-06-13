<%doc>
    Template used to render buttons (see utils/widgets.py)
</%doc>
% if elem.permitted(request.context, request):
    <a title='${elem.title}' href="#" onclick="${elem.onclick()}"
% if elem.css:
    class="${elem.css}"
% endif
>
      %if elem.icon:
          <i class='${elem.icon}'></i>
      % endif
      ${elem.label}
    </a>
% endif
