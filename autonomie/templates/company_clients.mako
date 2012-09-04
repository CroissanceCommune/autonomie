<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>${sortable("Code", "code")}</th>
            <th>${sortable("Entreprise", "name")}</th>
            <th>${sortable("Nom du contact principal", "contactLastName")}</th>
            <th style="text-align:center">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if clients:
            % for client in clients:
                <tr class='tableelement' id="${client.id}">
                    <td onclick="document.location='${request.route_path("client", id=client.id)}'" class="rowlink" >${client.code}</td>
                    <td onclick="document.location='${request.route_path("client", id=client.id)}'" class="rowlink" >${client.name}</td>
                    <td onclick="document.location='${request.route_path("client", id=client.id)}'" class="rowlink" >${client.contactLastName} ${client.contactFirstName}</td>
                    <td style="text-align:right">
                        ${table_btn(request.route_path("client", id=client.id), u"Voir/Éditer", u"Voir/Éditer ce client", icon=u"icon-pencil")}
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun client n'a été référencé pour l'instant
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(clients)}
</%block>
