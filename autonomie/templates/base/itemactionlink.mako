<%doc>
    Template used to render action buttons (see utils/widgets.py)
    item is the current item the action is made on
    elem is the current link object
</%doc>
% if elem.permitted(item, request):
    <a title='${elem.title}' href="${elem.url(item, request)}"
      %if elem.onclick():
          onclick="${elem.onclick()}"
      %endif
% if elem.css:
    class="${elem.css}"
       % endif
      >
      %if elem.icon:
        %if hasattr(elem.icon, "__iter__"):
            %for icon in elem.icon:
                <i class="${icon}"></i>
            % endfor
        %else:
          <i class='${elem.icon}'></i>
        % endif
      % endif
      <span class="visible-desktop hidden-tablet" style="display:inline">
      ${elem.label}
      </span>
    </a>
% endif
