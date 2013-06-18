<%inherit file="/admin/index.mako"></%inherit>
<%block name="css" >
<link href="${request.static_url('autonomie:static/css/admin.css')}" rel="stylesheet"  type="text/css" />
</%block>
<%block name='content'>
<div class='row'>
    <div class="span12">
        ${form|n}
    </div>
</div>
</%block>
