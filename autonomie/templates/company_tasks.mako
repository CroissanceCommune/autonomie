<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/utils.mako" import="format_customer" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='company_tasks_panel'>
% if not request.is_xhr:
<div class='row'>
    <div class='span12'>
        <div class='well tasklist' style="margin-top:10px" id='tasklist_container'>
% endif
            <div class='section-header'>Dernières activités</div>
            Afficher <select id='number_of_tasks'>
              % for i in (5, 10, 15, 50):
              <option value='${i}'
              % if tasks.items_per_page == i:
                selected=true
              % endif
              >
              ${i}
              </option>
              % endfor
            </select>
            éléments à la fois
            <table class='table table-stripped tasklist'>
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
            ${pager(tasks)}
% if not request.is_xhr:
</div>
</div>
</div>
% endif
</%block>
