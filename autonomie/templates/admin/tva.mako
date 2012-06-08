<%inherit file="/admin/index.mako"></%inherit>
<%block name='css'>
<style>
    .deformSeqItem{
        margin-bottom:5px;
        background-color:#eee;
    }
</style>
</%block>
<%block name='content'>
<div class='row'>
    <div class='span6 offset3'>
        ${html_form|n}
    </div>
</%block>
