<%doc>
    invoice template
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
                % if not task.model.has_been_validated() and not task.model.is_paid():
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
        <strong>Avoir N° </strong>${task.model.number}<br />
        % if task.model.invoice:
            <span  style='color:#999'> <strong style='color:#999'>Référence facture N° </strong>${task.model.invoice.number}</span> <br />
                <br />
            % endif
            <strong>Objet : </strong>${format_text(task.model.description)}<br />
        </%block>
        <%block name="notes_and_conditions">
        %if task.model.reimbursementConditions:
            ${table(u"Conditions de remboursement", task.model.reimbursementConditions)}
        % endif
        % if config.has_key('coop_reimbursement'):
            ${table(u"Mode de remboursement", config['coop_reimbursement'])}
        %endif
        </%block>
