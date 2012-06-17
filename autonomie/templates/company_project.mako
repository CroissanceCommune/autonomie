<%inherit file="base.mako"></%inherit>
<%namespace file="base/utils.mako" import="address" />
<%block name='content'>
<div class='row collapse' id='project-addphase'>
    <div class='span4 offset4'>
        <h3>Ajouter une phase</h3>
        <form class='navbar-form' method='POST' action="${request.route_path('company_project', id=project.id, _query=dict(action='addphase'))}">
            <input type='text' name='phase' />
            <button class='btn btn-primary' type='submit' name='submit' value='addphase'>Valider</button>
        </form>
        <br />
    </div>
</div>
    <div class='row collapse' id='project-description'>
        <div class="span2 offset2">
            <h3>Client</h3>
            ${address(project.client, "client")}
            %if project.type:
                <b>Type de projet :</b> ${project.type}
            % endif
            <br />
        </div>
        <div class="span5 offset2">
            <h3>Définition du projet</h3>
            ${project.definition}
        </div>
</div>
<div class='row'>
    <div class='span6 offset3'>
        ${html_form|n}
    </div>
</div>
</%block>
