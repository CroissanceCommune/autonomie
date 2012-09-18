# -*- coding: utf-8 -*-
<%doc>
    textarea for estimation/invoice lines
</%doc>
<textarea name="${field.name}"
% if hasattr(field, 'css_class'):
class="${field.css_class}"
% endif
>${cstruct}</textarea>
${field}
