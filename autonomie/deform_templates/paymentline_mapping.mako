# -*- coding: utf-8 -*-
<%doc>
Linesblock line representation
</%doc>
% for c in field.children:
    ${field.renderer(field.widget.item_template, field=c, cstruct=cstruct.get(c.name, null))|n}
% endfor
