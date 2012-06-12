<div class="deformFileupload">

  <input type="hidden" name="__start__" value="${field.name}:mapping"/>

    <input type="file" name="upload" class="${field.widget.css_class}" size="${field.widget.size}"  id="${field.oid}"/>
    %if cstruct.get('uid'):
      <div class="deformReplaces">
        <input type="hidden" name="uid" value="${cstruct['uid']}"
           id="${field.oid}-uid"/>
      </div>
        % if cstruct.get('preview_url'):
            <span class="help-block">
                <a href='${cstruct['preview_url']}'>${cstruct.get('filename')}</a>
            </span>
        % endif
    % endif
    <input type="hidden" name="__end__" value="${field.name}:mapping"/>
</div>

