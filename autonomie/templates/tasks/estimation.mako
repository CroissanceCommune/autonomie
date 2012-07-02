<%doc>
    estimation template
</%doc>
<%inherit file="/tasks/task.mako" />
<%namespace file="/base/utils.mako" import="print_date" />
<%namespace file="/base/utils.mako" import="format_amount" />
<%namespace file="/base/utils.mako" import="format_quantity" />
<%namespace file="/base/utils.mako" import="format_text" />
<%def name="table(title, datas)">
    <div class="title">
        ${title}
    </div>
    <div class='content'>
        ${format_text(datas)}
    </div>
</%def>
<%block name='header'>
<style>
    @page {
    size: a4 portrait;
    margin:1cm;
    margin-bottom:3.5cm;
    % if not task.model.has_been_validated() and not task.model.is_cancelled():
        background-image: url("${request.static_url('autonomie:static/watermark_estimation.jpg', _app_url='')}");
    % endif
    @frame footer {
    -pdf-frame-content: footer;
    bottom: 0cm;
    margin-left: 1cm;
    margin-right: 1cm;
    height:3cm;
    }
    }
</style>
</%block>
<%block name="information">
<strong>DEVIS N° </strong>${task.model.number}<br />
<strong>Objet : </strong>${format_text(task.model.description)}<br />
</%block>
<%block name="notes_and_conditions">
%if task.model.exclusions:
    ${table(u"Notes", task.model.exclusions)}
%endif
% if task.model.paymentDisplay != u"NONE":
    % if task.model.paymentDisplay == u"ALL":
        <% colspan = 3 %>
    %else:
        <% colspan = 1 %>
    % endif
    <div class='row'>
        <table class='lines span12'>
            <thead>
                <th colspan='${colspan}' style='text-align:left'>Conditions de paiement</th>
            </thead>
            <tbody>
                <tr>
                    <td colspan='${colspan}'>
                        ${task.model.paymentConditions}
                        <br />
                        % if task.model.deposit > 0 :
                            Un acompte, puis paiement en ${task.get_nb_payment_lines()} fois.
                        %else:
                            Paiement en ${task.get_nb_payment_lines()} fois.
                        %endif
                    </td>
                </tr>
                % if task.model.paymentDisplay == u"ALL":
                    ## l'utilisateur a demandé le détail du paiement
                    ## L'acompte à la commande
                    % if task.model.deposit > 0 :
                        <tr>
                            <td>Acompte</td>
                            <td>à la commande</td>
                            <td class='price'>${format_amount(task.compute_deposit())} €</td>
                        </tr>
                    % endif
                    ## Les paiements intermédiaires
                    % for line in task.model.payment_lines[:-1]:
                        <tr>
                            <td>${print_date(line.paymentDate)}</td>
                            <td>${line.description}</td>
                            %if task.model.manualDeliverables == 1:
                                <td>${format_amount(line.amount)} €</td>
                            %else:
                                <td class='price'>${format_amount(task.compute_line_amount())} €</td>
                            %endif
                        </tr>
                    % endfor
                    ## On affiche le solde qui doit être calculé séparément pour être sûr de tomber juste
                    <tr>
                        <td>
                            ${print_date(task.model.payment_lines[-1].paymentDate)}
                        </td>
                        <td>
                            ${format_text(task.model.payment_lines[-1].description)}
                        </td>
                        <td class='price'>
                            ${format_amount(task.compute_sold())} €
                        </td>
                    </tr>
                % endif
            </tbody>
        </table>
    %else:
        %if task.model.paymentConditions:
            ${table(u"Conditions de paiement", task.model.paymentConditions)}
        % endif
    </div>
% endif
% if config.has_key('coop_estimationfooter'):
    ${table(u"Acceptation du devis", config.get('coop_estimationfooter'))}
%endif
</%block>
