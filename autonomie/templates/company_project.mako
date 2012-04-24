<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    % if project is not UNDEFINED and project.id is not None:
    <li>
        <a class="btn-primary" title='Voir le projet' href='${request.route_path("company_project", cid=company.id, id=project.id)}'>
            Revenir à la fiche du projet
        </a>
        </li>
    % endif
    <li>
    <a class="btn-primary" title='Revenir à la liste des projets'  href='${request.route_path("company_projects", cid=company.id)}'>
        Revenir à la liste des projets
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
