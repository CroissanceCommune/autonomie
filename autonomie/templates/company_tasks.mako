<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_customer" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='company_tasks_panel'>
<div class='row'>
    <div class='span12'>
        <div class='well' style="margin-top:10px">
            <div class='section-header'>Dernières activités</div>
            <table class='table table-stripped'>
                <thead>
                    <th>
                        Projet
                    </th>
                    <th>
                        Client
                    </th>
                    <th>
                        Nom du document
                    </th>
                    <th>
                        Dernière modification
                    </th>
                </thead>
                <tbody>
                    % for task in tasks:
                        <tr>
                            <td>
                                ${format_project(task.project)}
                            </td>
                            <td>
                                ${format_customer(task.customer)}
                            </td>
                            <td>${task.name}</td>
                            <td>${api.format_status(task)}</td>
                            <td>
                                ${table_btn(request.route_path(task.type_, id=task.id), u"Voir", u"Voir ce document", icon=u"icon-search")}
                            </td>
                        </tr>
                    % endfor
                </tbody>
            </table>
            <a id="index_activities_previous">previous</a> 
            <a id="index_activities_next">next</a> 
        </div>
    </div>
</div>
</%block>
