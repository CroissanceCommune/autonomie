<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='row collapse' id='project-addphase'>
    <div class='span4'>
        <h3>Ajouter une phase</h3>
        <form class='navbar-form' method='POST' action="${request.route_path('company_project', id=project.id, _query=dict(action='addphase'))}">
            <input type='text' name='phase' />
            <button class='btn btn-primary' type='submit' name='submit' value='addphase'>Valider</button>
        </form>
        <br />
    </div>
</div>
<div class='row'>
    <div class='span6 offset3'>
        ${html_form|n}
    </div>
</div>
</%block>
