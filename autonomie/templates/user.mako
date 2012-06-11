<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a title='Éditer la fiche de l'utilisateur' href='${request.route_path("user", id=user.id)}'>
        Éditer ce compte
    </a>
    </li>
    <li>
    <a title='Revenir à la liste des utilisateurs'  href='${request.route_path("users")}'>
        Revenir à la liste
    </a>
    </li>
</ul>
</%block>
<%block name='content'>
<div class='row'>
    <div class='span3 offset2'>
        <a title='Éditer les informations de ce client'
            href='${request.route_path("user", id=user.id, _query=dict(action="edit"))}'
            class='btn btn-primary'>
            Éditer
        </a>
        <dl>
            % for label, value in ((u'Identifiant', user.login), (u"Nom", user.lastname), (u"Prénom", user.firstname), ("E-mail", user.email)):
                %if value:
                    <dt>${label}</dt>
                    <dd>${value}</dd>
                % endif
            % endfor
        </dl>
        <br />
        <br />
        % if len(user.companies) == 1:
            <h3>Entreprise</h3>
        %else:
            <h3>Entreprises</h3>
        % endif
        <br />
        % for company in user.companies:
            <a href="${request.route_path('company', id=company.id, _query={'action':'edit'})}">
                <strong>${company.name}</strong>
                <br />
                %if company.get_logo_filepath():
                    <img src="/assets/${company.get_logo_filepath()}" alt=""  width="250px" />
                %endif
            </a>
            <br />
            ${company.goal}
            <br />
        % endfor
    </div>
</div>
</%block>

