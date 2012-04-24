<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    % if client is not UNDEFINED and client.id is not None:
        <li>
        <a class="btn-primary" title='Voir le projet' href='${request.route_path("company_client", cid=company.id, id=client.id)}'>
            Revenir à la fiche du client
        </a>
        </li>
    %endif
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
