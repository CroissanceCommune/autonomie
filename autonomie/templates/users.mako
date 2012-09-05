<%doc>
    Directory templates, list users and companies
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>${sortable("Nom", "lastname")}</th>
            <th>${sortable("E-mail", "email")}</th>
            <th>Entreprises</th>
        </tr>
    </thead>
    <tbody>
        % if users:
            % for user in users:
                <tr>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >${api.format_account(user, reverse=True)}</td>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >${user.email}</td>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >
                        <ul>
                            % for company in user.companies:
                                <li>${company.name}</li>
                            % endfor
                        </ul>
                    </td>
                </tr>
            % endfor
        % else:
            <tr><td colspan='3'>Aucun utilisateur n'est présent dans la base</td></tr>
        % endif
</tbody></table>
${pager(users)}
</%block>
