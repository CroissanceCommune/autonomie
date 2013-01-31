<%doc>
    invoice template
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
                    background-image: url("${request.static_url('autonomie:static/watermark_invoice.jpg', _app_url='')}");
                % endif
                @frame footer {
                    -pdf-frame-content: footer;
                    bottom: 0cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    % if hasattr(task, "course") and task.course == 1 and config.has_key('coop_pdffootercourse'):
                        height:4cm;
                    % else:
                        height:3cm;
                    % endif
                }
            }
        </style>
</%block>
<%block name='information'>
<strong>Facture N°</strong>${task.officialNumber}<br />
<strong>Libellé : </strong>${task.number}<br />
<strong>Objet : </strong>${format_text(task.description)}<br />
</%block>
<%block name="notes_and_conditions">
%if task.paymentConditions:
    ${table(u"Conditions de paiement", task.paymentConditions)}
% endif
% if config.has_key('coop_invoicepayment'):
    <% paymentinfo = config.get('coop_invoicepayment')%>
    % if company.IBAN is not None:
        <% paymentinfo = paymentinfo.replace(u"%IBAN%", company.IBAN) %>
    % endif
    % if company.RIB is not None:
        <% paymentinfo = paymentinfo.replace(u"%RIB%", company.RIB) %>
    % endif
    % if company.name is not None:
        <% paymentinfo = paymentinfo.replace(u"%ENTREPRENEUR%", company.name) %>
    % endif
    ${table(u"Mode de paiement", paymentinfo)}
%endif
% if config.has_key('coop_invoicelate'):
    <% tolate = config.get('coop_invoicelate').replace(u"%ENTREPRENEUR%", company.name) %>
    ${table(u"Retard de paiement", tolate)}
% endif
</%block>
