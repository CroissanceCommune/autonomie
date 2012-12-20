<%inherit file="base.mako"></%inherit>
<%namespace file="base/utils.mako" import="format_text" />
<%block name='content'>
% if hasattr(project, "id") and project.id:
    <div class='row collapse' id='project-addphase'>
        <div class='span4 offset4'>
            <h3>Ajouter une phase</h3>
            <form class='navbar-form' method='POST' action="${request.route_path('project', id=project.id, _query=dict(action='addphase'))}">
                <input type='text' name='phase' />
                <button class='btn btn-primary' type='submit' name='submit' value='addphase'>Valider</button>
            </form>
            <br />
        </div>
    </div>
% endif
<div class='row collapse' id='project-description'>
        <div class="span8 offset2">
    <div class="well">
                    <h3>Client(s)</h3>
                    % for client in project.clients:
                        <div class='well'>
                            <address>
                                ${format_text(client.full_address)}
                            </address>
                        </div>
                    % endfor
        %if project.type:
            <b>Type de projet :</b> ${project.type}
        % endif
        <br />
        % if project.definition:
            <h3>Définition du projet</h3>
            ${project.definition}
        % endif
    </div>
</div>
</div>
<div class='row'>
    <div class='span6 offset3'>
        ${form|n}
    </div>
</div>
</%block>
