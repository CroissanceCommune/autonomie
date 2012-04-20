<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a class="btn-primary" title='Éditer les informations de ce client' style='margin:0px 10px 0px 250px;'
        href='${request.route_path("company_project", cid=company.id, id=project.id, _query=dict(edit=True))}'>
        Éditer
    </a>
    </li>
</ul>
</%block>
<%block name='content'>
<div class='container'>
    %for phase in project.phases:
        % if phase.name != 'default':
            <div class='label'>${phase.name}</div>
        % endif
        <div class='label'>Devis</div>
        <table class='table table-striped'>
            %for estimation in phase.estimations:
                <tr onclick="document.location = '${request.route_path("estimation", cid=company.id, id=project.id, taskid=estimation.IDTask)}'">
                    <td>${estimation.name}</td>
                    <td>${estimation.number}</td>
                    <td>${estimation.CAEStatus}</td>
                    <td>${estimation.customerStatus}</td>
                </tr>
            %endfor
        </table>
        <div class='label'>Facture(s)</div>
        <table class='table table-striped'>
            %for invoice in phase.invoices:
                <tr onclick="document.location = '${request.route_path("estimation", cid=company.id, id=project.id, taskid=invoice.IDTask)}'">
                    <td>${invoice.name}</td>
                    <td>${invoice.number}</td>
                    <td>${invoice.CAEStatus}</td>
                    <td>${invoice.customerStatus}</td>
                </tr>
            %endfor
        </table>
    %endfor
</div>
</%block>
