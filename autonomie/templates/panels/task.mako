<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>
<%doc>
    Task content rendering panel
    Only renders the content of the page
</%doc>
<%namespace file="/base/utils.mako" import="format_text" />
<div id='content'>
    <div class='header'>
        <img src='${api.img_url(company.header_file)}' alt='${company.name}'/>
    </div>
    <div class='row'>
        <div class='addressblock'>
            ${format_text(task.address)}
        </div>
    </div>
    <div class="informationblock">
        Le ${api.format_date(task.date, False)},
        <br />
        <%block name='information'>
        </%block>
        % if task.customer.intraTVA:
            <b>Numéro de TVA Intracommunautaire</b> : ${task.customer.intraTVA}
            <br />
        % endif
    </div>
    <div class='row'>
        <% groups = task.get_groups() %>
        % for group in groups:
            <% display_tvas_column = multiple_tvas and len(groups) == 1 and group.title == '' %>

            <% num_cols = 2 %>
            %if task.display_units == 1:
                <% colspan = 3 %>
                <% num_cols += 2 %>
            %else:
                <% colspan = 1 %>
            % endif
            % if display_tvas_column:
                <% num_cols += 1 %>
            % endif
            <table class="lines col-xs-12 table table-stripped">
                <thead>
                    % if group.title != '':
                        <tr>
                            <td colspan="${num_cols}"><h3>${group.title}</h3></td>
                        </tr>
                    % endif
                    % if group.description != "":
                        <tr class='group-description'>
                            <td colspan="${num_cols}">
                                ${format_text(group.description)}
                            </td>
                    </tr>
                    % endif
                    <tr>
                        <th class="description">Intitulé des postes</th>
                        %if task.display_units == 1:
                            <th class="unity">P.U.</th>
                            <th class="quantity">Qté</th>
                        % endif
                        <th class="price">Prix</th>
                        % if display_tvas_column:
                            <th class='tva'>Tva</th>
                        % endif
                    </tr>
                </thead>
                <tbody>
                    % for line in group.lines:
                        <tr>
                            <td class="description">${format_text(line.description, False)}</td>
                            %if task.display_units == 1:
                                <td class="unity">${api.format_amount(line.cost, trim=False, precision=5)|n}&nbsp;€</td>
                                <td class="quantity">${api.format_quantity(line.quantity)} ${line.unity}</td>
                            % endif
                            <td class="price">${api.format_amount(line.total_ht(), trim=False, precision=5)|n}&nbsp;€</td>
                            % if display_tvas_column:
                                <td class='tva'>
                                    % if line.tva>=0:
                                        ${api.format_amount(line.tva, precision=5)|n}&nbsp;%
                                    % endif
                                </td>
                            % endif
                        </tr>
                    % endfor
                    % if len(groups) > 1:
                        <tr>
                            <td colspan='${colspan}' class='rightalign'>
                                Sous-total HT
                            </td>
                            <td class='price'>
                                ${api.format_amount(group.total_ht(), trim=False, precision=5)|n}&nbsp;€
                            </td>
                            % if display_tvas_column:
                                <td></td>
                            % endif
                        </tr>
                    % endif
                % if len(groups) > 1:
                        </tbody>
                    </table>
                % endif
        % endfor
        % if len(groups) > 1:
            <table class='lines col-xs-12 table table-stripped'>
            <tbody>
        % endif
        <% display_tvas_column = multiple_tvas and len(groups) == 1 and group.title == '' %>

                % if task.expenses_ht not in (0, None):
                    <tr>
                        <td class='description' colspan='${colspan}'>
                            Frais forfaitaires
                        </td>
                        <td class="price">
                            ${api.format_amount(task.expenses_ht, precision=5)|n}&nbsp;€
                        </td>
                        % if display_tvas_column:
                            <td class='tva'>
                                ${api.format_amount(task.expenses_tva, precision=5)|n}&nbsp;%
                            </td>
                        % endif
                    </tr>
                % endif
                %if hasattr(task, "discounts") and task.discounts:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Total HT
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.groups_total_ht() + task.expenses_ht, trim=False, precision=5)|n}&nbsp;€
                        </td>
                        % if display_tvas_column:
                            <td></td>
                        % endif
                    </tr>
                    % for discount in task.discounts:
                        <tr>
                            <td colspan='${colspan}' class='description'>
                                ${format_text(discount.description)}
                            </td>
                            <td class='price'>
                                ${api.format_amount(discount.amount, precision=5)|n}&nbsp;€
                            </td>
                            % if display_tvas_column:
                                <td class='tva'>
                                    ${api.format_amount(discount.tva, precision=5)|n}&nbsp;%
                                </td>
                            % endif
                        </tr>
                    % endfor
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Total HT après remise
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.total_ht(), precision=5)|n}&nbsp;€
                        </td>
                        % if display_tvas_column:
                            <td></td>
                        % endif
                    </tr>
                % else:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Total HT
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.groups_total_ht() + task.expenses_ht, precision=5)|n}&nbsp;€
                        </td>
                        % if display_tvas_column:
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
                            % if tva>0:
                            <td colspan='${colspan}' class='rightalign'>
                                TVA (${api.format_amount(tva, precision=5)|n} %)
                            </td>
                            <td class='price'>
                                ${api.format_amount(tva_amount, precision=5)|n}&nbsp;€
                            </td>
                            % endif
                        </tr>
                    % endfor
                % endif
                %if task.expenses:
                    <tr>
                        <td colspan='${colspan}' class='rightalign'>
                            Frais réels
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.expenses_amount(), precision=5)|n}&nbsp;€
                        </td>
                    </tr>
                %endif
                <tr>
                    <td colspan='${colspan}' class='rightalign'>
                        Total TTC
                    </td>
                    <td class='price'>
                        ${api.format_amount(task.total(), precision=5)|n}&nbsp;€
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <%block name="notes_and_conditions">
    ## All infos beetween document lines and footer text (notes, payment conditions ...)
    </%block>
    % for mention in task.mentions:
        <div class="title">
            ${mention.title}
        </div>
        <div class='content'>
            ${format_text(mention.full_text)}
        </div>
    % endfor

</div>
## end of content
    <div
        class='row pdf_footer'
        id='commonfooter'
        ## In view_only only mode we switch footers by css, in pdf mode, we use frames (see templates/tasks/task.mako)
        % if not bulk and getattr(task, 'course', 0) == 1:
            style="display:none"
        % endif
        >
        ## The common footer
    % if config.has_key('coop_pdffootertitle'):
        <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
    %endif
    % if config.has_key('coop_pdffootertext'):
        ${format_text(config.get('coop_pdffootertext'))}
    % endif
</div>
<div
    class='row pdf_footer'
    id='coursefooter'
    ## In view_only only mode we switch footers by css, in pdf mode, we use frames (see templates/tasks/task.mako)
    % if not bulk and getattr(task, 'course', 0) != 1:
        style="display:none"
    % endif
    >
    ## The footer specific to courses (contains the additionnal text infos)
    % if config.has_key('coop_pdffootertitle'):
        <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
    %endif
    % if config.has_key('coop_pdffootercourse'):
        ${format_text(config.get('coop_pdffootercourse'))}<br />
    % endif
    % if config.has_key('coop_pdffootertext'):
        ${format_text(config.get('coop_pdffootertext'))}
    % endif
</div>
% if task.has_been_validated() or task.is_cancelled():
<div id='page-number'>
    Page <pdf:pagenumber/>/<pdf:pagecount/>
</div>
% endif
% if bulk is UNDEFINED or not bulk:
    % if config.has_key('coop_cgv') and config['coop_cgv']:
        <pdf:nextpage />
        <div id="cgv">
            ${format_text(config['coop_cgv'], False)}
        </div>
    % endif
    % if company.cgv:
        <pdf:nextpage />
        <div>
            ${format_text(company.cgv, False)}
        </div>
    % endif
% endif
