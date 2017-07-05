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
    estimation panel template
</%doc>
<%inherit file="/panels/task.mako" />
<%namespace file="/base/utils.mako" import="format_text" />
<%def name="table(title, datas, css='')">
    <div class="title ${css}">
        ${title}
    </div>
    <div class='content'>
        ${format_text(datas)}
    </div>
</%def>
<%block name="information">
<strong>DEVIS N° </strong>${task.internal_number}<br />
<strong>Objet : </strong>${format_text(task.description)}<br />
% if task.workplace:
    <strong>Lieu d'éxécution des travaux : </strong>
    <br />
    ${format_text(task.workplace)}
    <br />
% endif
% if config.get('coop_estimationheader'):
    ${format_text(config['coop_estimationheader'])}
% endif
</%block>
<%block name="notes_and_conditions">
%if task.exclusions:
    ${table(u"Notes", task.exclusions)}
%endif
% if task.paymentDisplay != u"NONE":
    % if task.paymentDisplay == u"ALL":
        <% colspan = 3 %>
    % elif task.paymentDisplay == u"ALL_NO_DATE":
        <% colspan = 2 %>
    %else:
        <% colspan = 1 %>
    % endif
    <div class='row'>
        <table class='lines col-md-12'>
            <thead>
                <th colspan='${colspan}' class='title' style='text-align:left'>Conditions de paiement</th>
            </thead>
            <tbody>
                <tr>
                    <td colspan='${colspan}'>
                        ${task.payment_conditions}
                        <br />
                        % if task.deposit > 0 :
                            Un acompte, puis paiement en ${task.get_nb_payment_lines()} fois.
                        %else:
                            Paiement en ${task.get_nb_payment_lines()} fois.
                        %endif
                    </td>
                </tr>
                % if task.paymentDisplay in (u"ALL", "ALL_NO_DATE"):
                    ## l'utilisateur a demandé le détail du paiement
                    ## L'acompte à la commande
                    % if task.deposit > 0 :
                        <tr>
                            <td
                                % if task.paymentDisplay == u"ALL":
                                    colspan=2
                                % endif
                                >Acompte à la commande</td>
                            <td class='price'>${api.format_amount(task.deposit_amount_ttc(), precision=5)|n}&nbsp;€</td>
                        </tr>
                    % endif
                    ## Les paiements intermédiaires
                    % for line in task.payment_lines[:-1]:
                        <tr>
                            % if task.paymentDisplay == u"ALL":
                                <td>${api.format_date(line.date)}</td>
                            % endif
                            <td>${line.description}</td>
                            %if task.manualDeliverables == 1:
                                <td>${api.format_amount(line.amount, precision=5)|n}&nbsp;€</td>
                            %else:
                                <td class='price'>${api.format_amount(task.paymentline_amount_ttc(), precision=5)|n}&nbsp;€</td>
                            %endif
                        </tr>
                    % endfor
                    ## On affiche le solde qui doit être calculé séparément pour être sûr de tomber juste
                    <tr>
                        % if task.paymentDisplay == u"ALL":
                            <td>
                                ${api.format_date(task.payment_lines[-1].date)}
                            </td>
                        % endif
                        <td>
                            ${format_text(task.payment_lines[-1].description)}
                        </td>
                        <td class='price'>
                            ${api.format_amount(task.sold(), precision=5)|n}&nbsp;€
                        </td>
                    </tr>
                % endif
            </tbody>
        </table>
    </div>
%else:
    %if task.payment_conditions:
        ${table(u"Conditions de paiement", task.payment_conditions)}
    % endif
% endif
% if config.get('coop_estimationfooter'):
    <div class='row keep_with_next'>
        ${table(u"Acceptation du devis", config.get('coop_estimationfooter'))}
    </div>
%endif
</%block>
<%block name="end_document">
<table style='width:100%; margin-bottom: 5px;'>
    <thead>
        <th style="width:65%">
        </th>
        <th style="width:35%" class='title'>
            Bon pour accord
        </th>
    </thead>
    <tbody>
        <tr>
            <td></td>
            <td class="content">
                Le :
            </td>
        </tr>
        <tr>
            <td></td>
            <td class="content">
                <i>Signature</i>
            <br />
            <br />
            <br />
            <br />
            <br />
            </td>
        </tr>
    </tbody>
</table>
</%block>
