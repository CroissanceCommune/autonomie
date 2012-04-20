<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a class="btn-primary" title='Revenir à la liste des projets'  href='${request.route_path("company_projects", cid=company.id)}'>
        Revenir à la liste
    </a>
    </li>
</ul>
</%block>
<%block name='content'>
<div class='container'>
    <div class='span5'>
        ${html_form|n}
    </div>
</div>
</%block>
