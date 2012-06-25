<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="urlbuild" />
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>${sortable("Code", "code")}</th>
            <th>${sortable("Nom", "name")}</th>
            <th>Client</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % if projects:
            % for project in projects:
                <tr class='tableelement' id="${project.id}">
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.code}</td>
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.name}</td>
                    <td onclick="document.location='${request.route_path("project", id=project.id)}'" class='rowlink'>${project.client.name}</td>
                    <td>
                        <div class='btn-group'>
                            % for btn in item_actions:
                                ${btn.render(request, project)|n}
                            % endfor
                        </div>
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
${pager(projects)}
% if html_form is not UNDEFINED:
    <div id='addform' style="overflow:hidden;">
        ${html_form|n}
    </div>
% endif
</%block>
<%block name='footerjs'>
% if html_form is not UNDEFINED:
    $( function() {
    $("#addform").dialog({ autoOpen: false,
    modal:true,
    width:"auto",
    height:"auto",
    autoResize:true,
    title:"Ajouter un Projet"
    })
    });
% endif
</%block>

