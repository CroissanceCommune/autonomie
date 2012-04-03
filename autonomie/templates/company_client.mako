<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a class="btn-primary" title='Revenir à la liste des clients'  href='${request.route_path("company_clients", cid=company.id)}'>
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
