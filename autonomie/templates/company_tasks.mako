<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_customer" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%block name='company_tasks_panel'>
% if not only_table:
<div class='row'>
    <div class='span12'>
        <div class='well tasklist' style="margin-top:10px"
            active_page="${active_page}"
            total_pages_nb="${total_pages_nb}">
            <div class='section-header'>Dernières activités</div>
% endif
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
% if not only_table:
            <div class="pagination">
            <ul>
            <li><a class="previous_btn_state">Previous</a></li>
            % for index in xrange(total_pages_nb):
            <li><a id="companytaskpage_${loop.index}">${loop.index + 1}</a></li>
            % endfor
            <li><a class="next_btn_state">Next</a></li>
            </ul>
            </div>
        </div>
    </div>
</div>
% endif
</%block>
