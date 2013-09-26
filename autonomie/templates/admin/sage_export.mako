<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
  Page allowing to export datas in a format readable by the Sage Treasury software
</%doc>
<%inherit file="/admin/index.mako"></%inherit>
<%block name='content'>
% if check_messages is not None:
    <div class='row'>
        <div class='span6 offset3'>
            <h2>${check_messages['title']}</h2>
        </div>
    </div>
    <p class='text-error'>
    % for message in check_messages['errors']:
        <b>*</b> ${message|n}<br />
    % endfor
    </p>
% endif
% for form in (all_form, period_form, from_invoice_number_form, invoice_number_form):
<div class='row'>
    <div class='span6 offset3'>
        ${form|n}
    </div>
</div>
% endfor
</%block>

