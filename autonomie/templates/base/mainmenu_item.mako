<%doc>
Main menu item template
</%doc>
% if elem.permitted(request.context, request):
<li>
    <a title='${elem.title}' href="${elem.url(request)}"
      %if elem.onclick():
          onclick="${elem.onclick()}"
      %endif
% if elem.css:
    class="${elem.css}"
       % endif
      >
      %if elem.icon:
          <i class='${elem.icon}'></i>
      % endif
      ${elem.label}
    </a>
</li>
% endif
