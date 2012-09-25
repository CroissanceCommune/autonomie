<%doc>
    Base template for task rendering
</%doc>
<%namespace file="/base/utils.mako" import="address" />
<%namespace file="/base/utils.mako" import="format_text" />
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="shortcut icon" href="" type="image/x-icon" />
        <meta name="description" comment="">
        <meta name="KEYWORDS" CONTENT="">
        <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
        <link href="${request.static_url('autonomie:static/css/pdf.css', _app_url='')}" rel="stylesheet"  type="text/css" />
        <%block name='header'>
        </%block>
    </head>
    <body>
        <div id='content'>
        <div class='header'>
            <img src='/assets/${company.get_header_filepath()}' alt='${company.name}' width='100%'/>
        </div>
        <div class='row'>
            <div class='addressblock'>
                ${api.format_date(task.taskDate, False)}
                <br />
                ${address(project.client, 'client')}
            </div>
        </div>
        <div class="informationblock">
            <%block name='information'>
            </%block>
        </div>
        %if task.displayedUnits == 1:
            <% colspan = 2 %>
        %else:
            <% colspan = 1 %>
        % endif
        <div class='row'>
            <table class="lines span12">
                <thead>
                    <tr>
                        <th class="description">Intitulé des postes</th>
                        %if task.displayedUnits == 1:
                            <th class="quantity">P.U. x Qté</th>
                        % endif
                        <th class="price">Prix</th>
                        % if multiple_tvas:
                            <th class='tva'>Tva</th>
                        % endif
                    </tr>
                </thead>
                <tbody>
                    % for line in task.lines:
                        <tr>
                            <td class="description">${format_text(line.description)}</td>
                            %if task.displayedUnits == 1:
                                <td class="quantity">${api.format_amount(line.cost)|n}&nbsp;€&nbsp;x&nbsp;${api.format_quantity(line.quantity)} ${api.format_unity(line.unity)}</td>
                            % endif
                            <td class="price">${api.format_amount(line.total_ht(), trim=False)|n}&nbsp;€</td>
                            % if multiple_tvas:
                                <td class='tva'>
                                    % if line.tva>=0:
                                        ${api.format_amount(line.tva)|n}&nbsp;%
                                    % endif
                                </td>
                            % endif
                        </tr>
                    % endfor
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Total HT
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.lines_total_ht(), trim=False)|n}&nbsp;€
                        </td>
                        % if multiple_tvas:
                            <td></td>
                        % endif
                    </tr>
                    %if hasattr(task, "discounts") and task.discounts:
                        % for discount in task.discounts:
                            <tr>
                                <td colspan='${colspan}' class='rightalign'>
                                    ${format_text(discount.description)}
                                </td>
                                <td class='price'>
                                    ${api.format_amount(discount.amount)|n}&nbsp;€
                                </td>
                                % if multiple_tvas:
                                    <td class='tva'>
                                        ${api.format_amount(discount.tva)|n}&nbsp;%
                                    </td>
                                % endif
                            </tr>
                        % endfor
                        <tr>
                            <td colspan='${colspan}' class='rightalign'>
                                Total HT après remise
                            </td>
                            <td class='price'>
                                ${api.format_amount(task.total_ht())|n}&nbsp;€
                            </td>
                            % if multiple_tvas:
                                <td></td>
                            % endif
                        </tr>
                    % endif
                    % if task.no_tva():
                        <tr>
                            <td colspan='${colspan + 1}'class='rightalign'>
                                TVA non applicable selon l'article 259b du CGI.
                            </td>
                        </tr>
                    % else:
                        %for tva, tva_amount in task.get_tvas().items():
                            <tr>
                                <td colspan='${colspan}' class='rightalign'>
                                    % if line.tva>0:
                                        TVA (${api.format_amount(tva)|n} %)
                                    % endif
                                </td>
                                <td class='price'>
                                    ${api.format_amount(tva_amount)|n}&nbsp;€
                                </td>
                            </tr>
                        % endfor
                    % endif
                    %if task.expenses:
                        <tr>
                            <td colspan='${colspan}' class='rightalign'>
                                Frais liés à la prestation
                            </td>
                            <td class='price'>
                                ${api.format_amount(task.expenses_amount())|n}&nbsp;€
                            </td>
                        </tr>
                    %endif
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Total TTC
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.total())|n}&nbsp;€
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <%block name="notes_and_conditions">
        ## All infos beetween document lines and footer text (notes, payment conditions ...)
        </%block>

    </div>
    ## end of content
        <div class='row' id='footer'>
            % if config.has_key('coop_pdffootertitle'):
                <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
            %endif
            % if hasattr(task, "course") and task.course == 1 and config.has_key('coop_pdffootercourse'):
                ${format_text(config.get('coop_pdffootercourse'))}<br />
            % endif
            % if config.has_key('coop_pdffootertext'):
                ${format_text(config.get('coop_pdffootertext'))}
            % endif
        </div>
    </body>
</html>
