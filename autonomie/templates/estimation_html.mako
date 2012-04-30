<%namespace file="/base/utils.mako" import="address" />
<%namespace file="/base/utils.mako" import="print_str_date" />
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="shortcut icon" href="" type="image/x-icon" />
        <meta name="description" comment="">
        <meta name="KEYWORDS" CONTENT="">
        <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
        <link href="${request.static_url('autonomie:static/css/pdf.css', _app_url='')}" rel="stylesheet"  type="text/css" />
        <style>
            @page {
                width:21cm;
                height:29.7cm;
                margin:1cm;
                @frame footer {
                    -pdf-frame-content: footer;
                    bottom: 0cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    height:3cm;
                }
            }
        </style>
    </head>
    <body>
        <div class='header'>
            <img src='/assets/${company.get_header_filepath()}' alt='${company.name}' width='100%'/>
        </div>
        <div class='row'>
            <div class='addressblock'>
                ${print_str_date(estimation.model.taskDate)}
                <br />
                ${address(project.client, 'client')}
            </div>
        </div>
        <div class="informationblock">
            <strong>DEVIS N° </strong>${estimation.model.number}<br />
            <strong>Objet : </strong>${format_text(estimation.model.description)}<br />
        </div>
        %if estimation.model.displayedUnits == 1:
            <% colspan = 2 %>
        %else:
            <% colspan = 1 %>
        % endif
        <div class='row'>
        <table class="lines span12">
            <thead>
                <tr>
                    <th class="description">Intitulé des postes</th>
                    %if estimation.model.displayedUnits == 1:
                        <th class="quantity">P.U. x Qté</th>
                    % endif
                    <th class="price">Prix</th>
                </tr>
            </thead>
            <tbody>
                % for line in estimation.model.lines:
                    <tr>
                        <td class="description">${format_text(line.description)}</td>
                        %if estimation.model.displayedUnits == 1:
                            <td class="quantity">${format_amount(line.cost)} € x ${format_quantity(line.quantity)} ${line.get_unity_label()}</td>
                        % endif
                        <td class="price">${format_amount(estimation.compute_line_total(line))} €</td>
                    </tr>
                % endfor
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        Total HT
                    </td>
                    <td class='price'>
                         ${format_amount(estimation.compute_lines_total())}
                     </td>
                 </tr>
                %if estimation.model.discountHT:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Remise commerciale
                        </td>
                        <td class='price'>
                            ${format_amount(estimation.model.discountHT)}
                        </td>
                    </tr>
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                         Total HT après remise
                        </td>
                        <td class='price'>
                            ${format_amount(estimation.compute_totalht())} €
                        </td>
                    </tr>

                % endif
                % if estimation.model.tva<0:
                    <tr>
                        <td colspan='${colspan + 1}'class='rightalign'>
                            TVA non applicable selon l'article 259b du CGI.
                        </td>
                    </tr>
                % else:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            TVA (${format_amount(estimation.model.tva)} %)
                        </td>
                        <td class='price'>
                            ${format_amount(estimation.compute_tva())} €
                        </td>
                    </tr>
                % endif
                %if estimation.model.expenses:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Frais liés à la prestation
                        </td>
                        <td class='price'>
                            ${format_amount(estimation.model.expenses)}
                        </td>
                    </tr>
                %endif
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        Total TTC
                    </td>
                    <td class='price'>
                        ${format_amount(estimation.compute_total())} €
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
        %if estimation.model.exclusions:
            ${table(u"Notes", estimation.model.exclusions)}
        %endif
        %if estimation.model.paymentConditions:
            ${table(u"Conditions de paiement", estimation.model.paymentConditions)}
        % endif
        % if estimation.model.paymentDisplay != u"NONE":
            % if estimation.model.paymentDisplay == u"ALL":
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
                        % if estimation.model.deposit > 0 :
                            Un accompte, puis paiement en ${estimation.get_nb_payment_lines()} fois.
                        %else:
                            Paiement en ${estimation.get_nb_payment_lines()} fois.
                        %endif
                    </td>
                </tr>
            % if estimation.model.paymentDisplay == u"ALL":
                ## l'utilisateur a demandé le détail du paiement
                    ## L'accompte à la commande
                     % if estimation.model.deposit > 0 :
                         <tr>
                             <td>Accompte</td>
                             <td>à la commande</td>
                             <td class='price'>${format_amount(estimation.model.compute_deposit())} €</td>
                         </tr>
                     % endif
                     ## Les paiements intermédiaires
                     % for line in estimation.model.payment_lines[:-1]:
                         <tr>
                             <td>${print_date(line.paymentDate)}</td>
                             <td>${line.description}</td>
                             %if estimation.model.manualDeliverables == 1:
                                 <td>${format_amount(line.amount)} €</td>
                             %else:
                                 <td class='price'>${format_amount(estimation.compute_line_amount())} €</td>
                             %endif
                         </tr>
                     % endfor
                     ## On affiche le solde qui doit être calculé séparément pour être sûr de tomber juste
                     <tr>
                        <td>
                            ${print_date(estimation.model.payment_lines[-1].paymentDate)}
                        </td>
                         <td>
                             ${format_text(estimation.model.payment_lines[-1].description)}
                        </td>
                        <td class='price'>
                            ${format_amount(estimation.compute_sold())} €
                        </td>
                    </tr>
            % endif
                </tbody>
            </table>
        </div>
        % endif
        % if config.has_key('coop_estimationfooter'):
            ${table(u"Acceptation du devis", config.get('coop_estimationfooter'))}
        %endif
        <div id="footer">
            % if config.has_key('coop_pdffootertitle'):
                <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
            %endif
            % if estimation.model.course == 1 and config.has_key('coop_pdffootercourse'):
                ${format_text(config.get('coop_pdffootercourse'))}<br />
            % endif
            % if config.has_key('coop_pdffootertext'):
                ${format_text(config.get('coop_pdffootertext'))}
            % endif
        </div>
    </body>
</html>
