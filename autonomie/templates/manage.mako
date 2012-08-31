<%doc>
    Template for the page showing the document waiting for approval
</%doc>
<%inherit file="/base.mako"></%inherit >
<%block name="content">
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>Entreprise</th>
            <th>Nom du document</th>
            <th>Statut</th>
        </tr>
    </thead>
    <tbody>
% for task in tasks:
    <tr>
        <td onclick="document.location='${task.url}'" class='rowlink'>
            ${task.get_company().name}
        </td>
        <td onclick="document.location='${task.url}'" class='rowlink'>
            ${task.name}
        </td>
        <td onclick="document.location='${task.url}'" class='rowlink'>
            ${api.format_status(task)}
        </td>
    </tr>
% endfor
    </tbody>
</table>

</%block>
