<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="urlbuild" />
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>${sortable(u"Code", "code")}</th>
            <th>${sortable(u"Nom", "name")}</th>
            <th>${sortable(u"Client", "client")}</th>
            <th style="text-align:center">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for project in records:
                <tr class='tableelement' id="${project.id}">
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.code}</td>
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.name}</td>
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.client.name}</td>
                    <td style="text-align:right">
                        % for btn in item_actions:
                            ${btn.render(request, project)|n}
                        % endfor
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun projet n'a été créé pour l'instant
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(records)}
</%block>
