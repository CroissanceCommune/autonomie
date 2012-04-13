<%doc>
Select field for unity configuration
</%doc>
<select name="${field.name}" class='span2'>
% for value, description in field.widget.values:
    <option value="${value}" \
% if value == cstruct:
selected='selected' \
% endif
>${description}</option>
% endfor
</select>
