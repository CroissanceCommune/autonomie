# -*- coding: utf-8 -*-
<%doc>
    Static div container used to display the list of tva amounts
</%doc>
<%def name='esc(datas)'><%text>${</%text>${datas}<%text>}</%text>\
</%def>
<script id="tvaTmpl" type="text/x-jquery-tmpl">
<div class='control-label'>
Dont TVA à ${esc('label')}
</div>
<div class='controls'>
    <div class='input'>${esc('value')}</div>
</div>
</script>
<div class='control-group estimationamounts offset8' id='total_ttc'>
    <div class='control-label'>
        Total TTC
    </div>
    <div class='controls'>
        <div class='input'></div>
    </div>
</div>
<div class='control-group estimationamounts offset8' id='tvalist'>
</div>
