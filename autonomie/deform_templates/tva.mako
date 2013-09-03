# -*- coding: utf-8 -*-
<%doc>
Select for tva amount
</%doc>
<select name="${field.name}" id="${field.oid}"
% if hasattr(field.widget, "css_class"):
class="${field.widget.css_class}"
% endif
>
% for value, description in values:
<option
%if value == cstruct:
selected="selected"
% endif
 value="${value}">${description}</option>
% endfor
</select>
<script>
 deform.addCallback(
    "${field.oid}",
    function (oid) {
      $('#' + oid + " select").change(function(){
          onTvaSelect(this);
          var row = $(this).parent().parent();
          $(Facade).trigger("linechange", row);
          $(Facade).trigger("totalchange", row);
      })
    });
</script>
