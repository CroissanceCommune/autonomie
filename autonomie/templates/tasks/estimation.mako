<%doc>
    estimation template
</%doc>
<%inherit file="/tasks/task.mako" />
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
    % if not task.has_been_validated() and not task.is_cancelled():
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
<strong>DEVIS N° </strong>${task.number}<br />
<strong>Objet : </strong>${format_text(task.description)}<br />
</%block>
<%block name="notes_and_conditions">
%if task.exclusions:
    ${table(u"Notes", task.exclusions)}
%endif
% if task.paymentDisplay != u"NONE":
    % if task.paymentDisplay == u"ALL":
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
                        ${task.paymentConditions}
                        <br />
                        % if task.deposit > 0 :
                            Un acompte, puis paiement en ${task.get_nb_payment_lines()} fois.
                        %else:
                            Paiement en ${task.get_nb_payment_lines()} fois.
                        %endif
                    </td>
                </tr>
                % if task.paymentDisplay == u"ALL":
                    ## l'utilisateur a demandé le détail du paiement
                    ## L'acompte à la commande
                    % if task.deposit > 0 :
                        <tr>
                            <td>Acompte</td>
                            <td>à la commande</td>
                            <td class='price'>${api.format_amount(task.deposit_amount())|n}&nbsp;€</td>
                        </tr>
                    % endif
                    ## Les paiements intermédiaires
                    % for line in task.payment_lines[:-1]:
                        <tr>
                            <td>${api.format_date(line.paymentDate)}</td>
                            <td>${line.description}</td>
                            %if task.manualDeliverables == 1:
                                <td>${api.format_amount(line.amount)|n}&nbsp;€</td>
                            %else:
                                <td class='price'>${api.format_amount(task.paymentline_amount())|n}&nbsp;€</td>
                            %endif
                        </tr>
                    % endfor
                    ## On affiche le solde qui doit être calculé séparément pour être sûr de tomber juste
                    <tr>
                        <td>
                            ${api.format_date(task.payment_lines[-1].paymentDate)}
                        </td>
                        <td>
                            ${format_text(task.payment_lines[-1].description)}
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.sold())|n}&nbsp;€
                        </td>
                    </tr>
                % endif
            </tbody>
        </table>
    %else:
        %if task.paymentConditions:
            ${table(u"Conditions de paiement", task.paymentConditions)}
        % endif
    </div>
% endif
% if config.has_key('coop_estimationfooter'):
    ${table(u"Acceptation du devis", config.get('coop_estimationfooter'))}
%endif
</%block>
