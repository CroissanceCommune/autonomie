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
%if elapsed_invoices:
    <div class='row'>
        <div class=''>
            <div class="ui-widget">
                <div class="ui-state-error ui-corner-all">
                  <p>
                  <span class="ui-icon ui-icon-alert">
                    </span>
                    <strong>
                        Les factures suivantes demandent votre attention, le paiement a plus de 45 jours de retard.</>
                        </strong>
                  </p>
                </div>
              </div>
              <a class='btn btn-primary' href="${request.route_path('company_invoices', cid=company.id)}">
                  Liste des factures
              </a>
            <table class='table table-stripped'>
                <thead>
                    <th>Numéro de facture</th>
                    <th>Émise le</th>
                    <th>Nom</th>
                    <th>Client</th>
                    <th>Total HT</th>
                    <th>TVA</th>
                </thead>
                <tbody>
                % for invoice in elapsed_invoices:
                    <tr>
                        <td>
                            ${invoice.model.officialNumber}
                            </td>
                            <td>
                            ${print_date(invoice.model.taskDate)}
                        </td>
                        <td>
                                <blockquote>
                                    <a href="${request.route_path('invoice', cid=company.id, id=invoice.model.project.id, taskid=invoice.model.IDTask)}" title='Voir le document'>
                                        ${invoice.model.number}<br />
                                    </a>
                                    <small>Projet : ${format_project(invoice.model.project, company)}</small>
                                </blockquote>
                        </td>
                        <td>
                            ${format_client(invoice.model.project.client, company)}
                        </td>
                        <td>
                            ${format_amount(invoice.compute_totalht())} € HT
                        </td>
                        <td>
                            ${format_amount(invoice.compute_tva())} €
                        </td>
                    </tr>
                % endfor
            </tbody>
                </table>
            </div>
        </div>
    %endif
    <div class='row'>
        <h3>Dernières activités</h3>
        <table class='table table-stripped'>
            <thead>
                <th>
                    Nom du projet
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
                        ${format_project(task.project, company)}
                    </td>
                    <td>${task.name}</td>
                    <td>${task.get_status_str()}</td>
                </tr>
            % endfor
            </tbody>
        </table>
    </div>
    </%block>
