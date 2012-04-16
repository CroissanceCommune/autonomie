# -*- coding: utf-8 -*-
<%
    cl = "control-group "
    if field.schema.css_class:
        cl += field.schema.css_class
    if field.error and not field.widget.hidden and not field.typ.__class__.__name__ == 'Mapping':
        cl += " error"
%>
<div class="${cl}" id="${field.oid}">
    ${field.serialize(cstruct)|n}
% if field.error and not field.widget.hidden and not field.typ.__class__.__name__ == 'Mapping':
    <br />
    <span class='help-inline'>
    %for msg in field.error.messages():
        <span class="error">${msg}</span>
    %endfor
</span>
% endif
</div>
