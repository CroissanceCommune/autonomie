# -*- coding: utf-8 -*-
%if field.error:
    <div class='row estimationline' style="background-color:#d54836" id="${field.oid}">
    %else:
        <div class='row estimationline' id="${field.oid}">
    %endif
    ${field.serialize(cstruct)|n}
    <div class='span1'>
        <button type='button' class='close' onclick="$(this).parent().parent().remove();">x</button>
    </div>
</div>

