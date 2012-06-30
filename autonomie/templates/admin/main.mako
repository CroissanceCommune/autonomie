<%inherit file="/admin/index.mako"></%inherit>
<%block name="headjs">
<script type="text/javascript" src="${request.static_url('deform:static/tinymce/jscripts/tiny_mce/tiny_mce.js')}"></script>
</%block>
<%block name='content'>
<div class='row'>
    <div class="span6 offset3">
        ${html_form|n}
    </div>
</div>

</%block>
