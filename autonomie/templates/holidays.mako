<%doc>
Template for holidays search
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="print_date" />
<%block name='content'>
<div class='row' style="padding-top:10px;">
    <div class='span6 offset3'>
        ${form|n}
        %if start_date and end_date:
            <h3>Congès entre le ${print_date(start_date)} et le ${print_date(end_date)}</h3>
        % endif
    </div>
</div>
<div class='row'>
    <div class='span6 offset3'>
        % if holidays:
        % for holiday in holidays:
            %if holiday.user:
                ${api.format_account(holiday.user)} : du ${print_date(max(holiday.start_date, start_date))} au ${print_date(min(holiday.end_date, end_date))}
                <br />
            % endif
        % endfor
    %else:
        Aucun congés n'a été déclaré sur cette période
    %endif
    </div>
</div>
</%block>
