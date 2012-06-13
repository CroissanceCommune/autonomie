<%doc>
Toggle link template
</%doc>
% if elem.permitted(request.context, request):
   <a title='${elem.title}' href="#" data-toggle='collapse' data-target='#${elem.target}'
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
