%if field.schema.css_class:
    <div class="${field.schema.css_class}" id="${field.oid}">
%else:
    <div  id="${field.oid}">
% endif
    ${field.serialize(cstruct)|n}
% if field.error and not field.widget.hidden and not field.typ.__class__.__name__ == 'Mapping':
    <br />
    %for msg in field.error.messages():
        <p class="${field.widget.error_class}">${msg}</p>
    %endfor
% endif
</div>
