<%inherit file="/base.mako"></%inherit>
<%block name="actionmenu">
<ul class='nav nav-pills'>
    <li>
        <a title="Revenir à la liste" href="${request.route_path('operations')}">
            Revenir à la liste
        </a>
    </li>
</ul>
</%block>
<%block name='content'>
<div class='row'>
    <div class="span6 offset3">
        ${html_form|n}
    </div>
</div>
</%block>
