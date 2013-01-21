<%doc>
    Simple page for form rendering
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
<div class="span6 offset2">
    ${form|n}
</div>
</%block>
