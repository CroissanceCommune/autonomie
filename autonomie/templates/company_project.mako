<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    % if project is not UNDEFINED and project.id is not None:
    <li>
        <a title='Voir le projet' href='${request.route_path("company_project", cid=company.id, id=project.id)}'>
            Revenir à la fiche du projet
        </a>
        </li>
    % endif
    <li>
    <a title='Revenir à la liste des projets'  href='${request.route_path("company_projects", cid=company.id)}'>
        Revenir à la liste des projets
    </a>
    </li>
</ul>
</%block>
<%block name='content'>
<div class='row'>
    <div class='span6 offset3'>
        ${html_form|n}
    </div>
</div>
</%block>
