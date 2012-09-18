# -*- coding: utf-8 -*-
<%doc>
    textarea for estimation/invoice lines
</%doc>
<textarea name="${field.name}"
% if hasattr(field.widget, 'css_class'):
class="${field.widget.css_class}"
% endif
>${cstruct}</textarea>
