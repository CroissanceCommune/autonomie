<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
  Template that display the list of expenses
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
% if conf_msg is not UNDEFINED:
    <br /><br />
    <div class='row'>
        <div class='span6 offset3'>
            <div class="alert alert-error">
                ${conf_msg}
            </div>
        </div>
    </div>
% else:
    % for year, values in expense_sheets.items():
            <div class='section-header'>
                <a href="#" data-toggle='collapse' data-target='#year_${year}'>
                    <div>
                        <i style="vertical-align:middle" class="icon-folder-open"></i>&nbsp;${year}
                    </div>
                </a>
            </div>
            % if year == current_year:
                <div class="section-content in collapse" id='year_${year}'>
            %else:
                <div class="section-content collapse" id='year_${year}'>
            %endif
        % for user, expenses in values:
        <table class="table table-condensed table-bordered">
            <caption>
                <b>Feuille de notes de frais de ${api.format_account(user)}</b>
                ${user_buttons[user.id].render(request)|n}
            </caption>
        <thead>
            <th>Période</th>
            <th>Statut</th>
            <th>Actions</th>
        </thead>
        <tbody>
            % for expense in expenses:
                <tr><td>${api.month_name(expense.month)} ${expense.year}</td>
                    <td>${api.format_expense_status(expense)}</td>
                    <td style='text-align:right'>
                        <a class='btn' href="${request.route_path('expense', id=expense.id)}"><i class='icon icon-search'></i>Voir</a>
                        <a class='btn' href="${request.route_path('expensexlsx', id=expense.id)}"><i class='icon icon-file'></i>Export</a>
                    </td>
                </tr>
            % endfor
            % if not expenses:
                <tr><td colspan='3'>Il n'y a aucun document</td></tr>
            % endif
        </tbody>
    </table>
    % endfor
</div>
    % endfor
% endif
</%block>
