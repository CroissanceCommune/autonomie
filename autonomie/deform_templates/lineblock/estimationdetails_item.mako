# -*- coding: utf-8 -*-
%if field.title:
    % if field.widget.__dict__.has_key('before'):
        ${field.renderer(field.widget.before, options=field.widget.before_options)|n}
     % endif
     <div class='control-group estimationamounts'>
        <label for="${field.oid}" class="control-label">${field.title}</label>
        <div class="controls" id="${field.oid}">
            ${field.serialize(cstruct).strip()|n}
            % if field.error and not field.widget.hidden and not field.typ.__class__.__name__=='Mapping':
                <span class="help-inline">
                    % for msg in field.error.messages():
                        <span class='error'>${_(msg)}</span>
                    % endfor
                </span>
            % endif
            % if field.description:
                <span class="help-block">
                    ${field.description}
                </span>
            % endif
        </div>
    </div>
    % if field.widget.__dict__.has_key('after'):
        ${field.renderer(field.widget.after, options=field.widget.after_options)|n}
    % endif
%else:
    ${field.serialize(cstruct).strip()|n}
% endif
