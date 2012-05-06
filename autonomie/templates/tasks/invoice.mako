<%doc>
    invoice template
</%doc>
<%inherit file="/tasks/task.mako" />
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
<%block name='header'>
        <style>
            @page {
                size: a4 portrait;
                margin:1cm;
                margin-bottom:3.5cm;
                % if not task.model.is_valid():
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
</%block>
        <%block name='information'>
            <strong>Facture N° </strong>${task.model.number}<br />
            <span  style='color:#999'> <strong style='color:#999'>Référence devis N° </strong>${task.model.number}</span> <br />
            <br />
            <strong>Objet : </strong>${format_text(task.model.description)}<br />
        </%block>
        <%block name="notes_and_conditions">
        %if task.model.paymentConditions:
            ${table(u"Conditions de paiement", task.model.paymentConditions)}
        % endif
        % if config.has_key('coop_invoicepayment'):
            <% paymentinfo = config.get('coop_invoicepayment').replace("%ENTREPRENEUR%", company.name).replace("%RIB%", company.RIB).replace("%IBAN%", company.IBAN) %>
            ${table(u"Mode de paiement", paymentinfo)}
        %endif
        % if config.has_key('coop_invoicelate'):
            <% tolate = config.get('coop_invoicelate').replace("%ENTREPRENEUR%", company.name) %>
            ${table(u"Retard de paiement", tolate)}
        % endif
        </%block>

        <div id="footer">
            % if config.has_key('coop_pdffootertitle'):
                <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
            %endif
            % if task.model.course == 1 and config.has_key('coop_pdffootercourse'):
                ${format_text(config.get('coop_pdffootercourse'))}<br />
            % endif
            % if config.has_key('coop_pdffootertext'):
                ${format_text(config.get('coop_pdffootertext'))}
            % endif
        </div>
    </body>
</html>
