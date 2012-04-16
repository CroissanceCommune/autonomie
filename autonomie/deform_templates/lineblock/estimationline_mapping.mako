# -*- coding: utf-8 -*-
<%doc>
Linesblock line representation
</%doc>
<input type="hidden" name="__start__" value="${field.name}:mapping"/>
% for c in field.children:
    ${field.renderer(field.widget.item_template, field=c, cstruct=cstruct.get(c.name, null))|n}
% endfor
<div class='span1 offset1 linetotal'>
    <div class='input'></div>
</div>
<input type="hidden" name="__end__" value="${field.name}:mapping"/>
