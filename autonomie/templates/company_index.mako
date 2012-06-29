<%doc>
    Company index page shows last activities and elapsed invoices
</%doc>
<%namespace file="/base/utils.mako" import="print_date" />
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_client" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="format_amount" />
<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='row'>
    <div class='span4'>
        %if elapsed_invoices:
        <div class='well' style="margin-top:10px">
            <div class='section-header'>Factures en retard
            </div>
            <a class='btn btn-primary'
                href="${request.route_path('company_invoices', id=company.id, _query=dict(paid="notpaid"))}">Voir</a>
            <table class='table table-stripped'>
                <thead>
                    <th>Numéro</th>
                    <th>Client</th>
                    <th>Total</th>
                </thead>
                <tbody>
                    % for invoice in elapsed_invoices:
                        <tr>
                            <td>
                                ${invoice.model.officialNumber}
                            </td>
                            <td>
                                ${format_client(invoice.model.project.client)}
                            </td>
                            <td>
                                ${format_amount(invoice.compute_total())} €
                            </td>
                        </tr>
                    % endfor
                </tbody>
            </table>
        </div>
        %endif
    </div>
        <div class='span6 offset1'>
            % if request.config.has_key('welcome'):
                <p>
                    ${format_text(request.config['welcome'])}
                </p>
            % endif
        </div>
</div>

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
                        <td>${task.name}</td>
                        <td>${task.get_status_str()}</td>
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
    </div>
</div>
</%block>
