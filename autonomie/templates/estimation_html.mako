<%namespace file="/base/utils.mako" import="address" />
<%namespace file="/base/utils.mako" import="print_str_date" />
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
    </head>
    <body>
        <div class='header'>
            <img src='/assets/${company.get_header_filepath()}' alt='${company.name}' />
        </div>
        <div class='addressblock'>
            ${print_str_date(estimation.model.taskDate)}
            <br />
            ${address(project.client, 'client')}
        </div>
        <div class="informationblock">
            <strong>DEVIS N° </strong>${estimation.model.number}<br />
            <strong>Objet : </strong>${format_text(estimation.model.description)}<br />
        </div>
        %if estimation.model.displayedUnits == 1:
            <% colspan = '2' %>
        %else:
            <% colspan = "1" %>
        % endif
        <table class="estimationlines">
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
                            <td class="quantity">${format_amount(line.cost)} € x ${format_quantity(line.quantity)} x ${line.get_unity_label()}</td>
                        % endif
                        <td class="price">${format_amount(estimation.compute_line_total(line))} €</td>
                    </tr>
                % endfor
                %if estimation.model.discountHT:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Remise commerciale
                        </td>
                        <td class='price'>
                            ${format_amount(estimation.model.discountHT)}
                        </td>
                    </tr>
                %endif
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        Total HT
                    </td>
                    <td class='price'>
                    ${format_amount(estimation.compute_totalht())} €
                    </td>
                </tr>
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        TVA (${format_amount(estimation.model.tva)} %)
                    </td>
                    <td class='price'>
                        ${format_amount(estimation.compute_tva())} €
                    </td>
                </tr>
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
        %if estimation.model.exclusions:
            ${table(u"Notes", estimation.model.exclusions)}
        %endif
        %if estimation.model.paymentConditions:
            ${table(u"Conditions de paiement", estimation.model.paymentConditions)}
        % endif
        % if config.has_key('coop_estimationfooter'):
            ${table(u"Acceptation du devis", config.get('coop_estimationfooter'))}
        %endif
    </body>
</html>
