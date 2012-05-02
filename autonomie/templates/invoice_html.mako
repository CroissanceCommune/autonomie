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
                size: a4 portrait;
                margin:1cm;
                margin-bottom:2.5cm;
                % if not invoice.model.is_valid():
                    background-image: url("${request.static_url('autonomie:static/watermark_invoice.jpg', _app_url='')}");
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
    </head>
    <body>
        <div class='header'>
            <img src='/assets/${company.get_header_filepath()}' alt='${company.name}' width='100%'/>
        </div>
        <div class='row'>
            <div class='addressblock'>
                ${print_str_date(invoice.model.taskDate)}
                <br />
                ${address(project.client, 'client')}
            </div>
        </div>
        <div class="informationblock">
            <strong>Facture N° </strong>${invoice.model.number}<br />
            <span  style='color:#999'> <strong style='color:#999'>Référence devis N° </strong>${invoice.model.number}</span> <br />
            <br />
            <strong>Objet : </strong>${format_text(invoice.model.description)}<br />
        </div>
        %if invoice.model.displayedUnits == 1:
            <% colspan = 2 %>
        %else:
            <% colspan = 1 %>
        % endif
        <div class='row'>
        <table class="lines span12">
            <thead>
                <tr>
                    <th class="description">Intitulé des postes</th>
                    %if invoice.model.displayedUnits == 1:
                        <th class="quantity">P.U. x Qté</th>
                    % endif
                    <th class="price">Prix</th>
                </tr>
            </thead>
            <tbody>
                % for line in invoice.model.lines:
                    <tr>
                        <td class="description">${format_text(line.description)}</td>
                        %if invoice.model.displayedUnits == 1:
                            <td class="quantity">${format_amount(line.cost)} € x ${format_quantity(line.quantity)} ${line.get_unity_label()}</td>
                        % endif
                        <td class="price">${format_amount(invoice.compute_line_total(line))} €</td>
                    </tr>
                % endfor
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        Total HT
                    </td>
                    <td class='price'>
                         ${format_amount(invoice.compute_lines_total())}
                     </td>
                 </tr>
                %if invoice.model.discountHT:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Remise commerciale
                        </td>
                        <td class='price'>
                            ${format_amount(invoice.model.discountHT)}
                        </td>
                    </tr>
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                         Total HT après remise
                        </td>
                        <td class='price'>
                            ${format_amount(invoice.compute_totalht())} €
                        </td>
                    </tr>

                % endif
                % if invoice.model.tva<0:
                    <tr>
                        <td colspan='${colspan + 1}'class='rightalign'>
                            TVA non applicable selon l'article 259b du CGI.
                        </td>
                    </tr>
                % else:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            TVA (${format_amount(invoice.model.tva)} %)
                        </td>
                        <td class='price'>
                            ${format_amount(invoice.compute_tva())} €
                        </td>
                    </tr>
                % endif
                %if invoice.model.expenses:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Frais liés à la prestation
                        </td>
                        <td class='price'>
                            ${format_amount(invoice.model.expenses)} €
                        </td>
                    </tr>
                %endif
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        Total TTC
                    </td>
                    <td class='price'>
                        ${format_amount(invoice.compute_total())} €
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
        %if invoice.model.paymentConditions:
            ${table(u"Conditions de paiement", invoice.model.paymentConditions)}
        % endif
        % if config.has_key('coop_invoicepayment'):
            <% paymentinfo = config.get('coop_invoicepayment').replace("%ENTREPRENEUR%", company.name).replace("%RIB%", company.RIB).replace("%IBAN%", company.IBAN) %>
            ${table(u"Mode de paiement", paymentinfo)}
        %endif
        % if config.has_key('coop_invoicelate'):
            <% tolate = config.get('coop_invoicelate').replace("%ENTREPRENEUR%", company.name) %>
            ${table(u"Retard de paiement", tolate)}
        % endif
        <div id="footer">
            % if config.has_key('coop_pdffootertitle'):
                <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
            %endif
            % if invoice.model.course == 1 and config.has_key('coop_pdffootercourse'):
                ${format_text(config.get('coop_pdffootercourse'))}<br />
            % endif
            % if config.has_key('coop_pdffootertext'):
                ${format_text(config.get('coop_pdffootertext'))}
            % endif
        </div>
    </body>
</html>
