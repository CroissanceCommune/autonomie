<%doc>
    Template for the page showing the document waiting for approval
</%doc>
<%inherit file="/base.mako"></%inherit >
<%block name="content">
<br />
<h3>Devis/Factures/Avoirs</h3>
<table class="table table-striped table-condensed table-hover table-bordered">
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
<br />
<h3>Feuilles de notes de frais</h3>
<table class="table table-striped table-condensed table-hover table-bordered">
    <thead>
        <tr>
            <th>Période</th>
            <th>Statut</th>
        </tr>
    </thead>
    <tbody>
% for expense in expenses:
    <tr>
        <td onclick="document.location='${expense.url}'" class='rowlink'>
            ${api.month_name(expense.month)} ${expense.year}
        </td>
        <td onclick="document.location='${expense.url}'" class='rowlink'>
            ${api.format_expense_status(expense)}
        </td>
    </tr>
% endfor
    </tbody>
</table>
</%block>
