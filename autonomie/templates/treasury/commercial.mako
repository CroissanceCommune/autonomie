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

<%inherit file="/base.mako"></%inherit>
<%block name='content'>
<div class='row'>
<div class='col-md-8 col-md-offset-2'>
<table class='table table-striped table-bordered' style="margin-top:15px">
<tr><td><b>Nombre de devis rédigés</b></td><td><b>${estimations}</b></td></tr>
<tr><td><b>Nombre de devis concrétisés</b></td><td><b>${validated_estimations}</b></td></tr>
<tr><td><b>Nombre de client</b></td><td><b>${customers}</b></td></tr>
</table>
</div>
</div>
<div class='row'>
    <div class='col-md-2 col-md-offset-8'>
        ${year_form.render()|n}
    </div>
</div>
<div class='row'>
    <table class='table table-striped table-bordered' style="margin-top:15px">
        <thead>
            <th>Description</th>
            % for i in range(1, 13):
                <th>${api.month_name(i)}</th>
            % endfor
            <th>Total annuel</th>
        </thead>
        <tbody>
            <tr><td>CA prévisionnel</td>
                % for i in range(1, 13):
                    <% turnover = turnover_projections.get(i) %>
                        % if turnover:
                            <td id='ca_prev_${i}' title='${turnover.comment}'>
                                ${api.format_amount(turnover.value, trim=True, precision=5)|n}
                        % else:
                            <td id='ca_prev_${i}'>
                        % endif
                        <a href='#setform'
                            % if turnover:
                                title='${turnover.comment}' onclick='setTurnoverProjectionForm("${i}", "${turnover.value/100.0}", this);'>
                            % else:
                                onclick='setTurnoverProjectionForm("${i}");'>
                            % endif
                            <i class="glyphicon glyphicon-pencil"></i>
                        </a>
                    </td>
                % endfor
                <td>
                    ${api.format_amount(turnover_projections['year_total'], trim=True, precision=5)|n}
                </td>
            </tr>
            <tr><td>CA réalisé</td>
                % for i in range(1, 13):
                    <td>${api.format_amount(turnovers[i], trim=True, precision=5)|n}</td>
                % endfor
                <td>
                    ${api.format_amount(turnovers['year_total'], trim=True, precision=5)|n}
                </td>
            </tr>
            <tr><td>Écart</td>
                % for i in range(1, 13):
                    <td id='gap_${i}'>
                        ${api.format_amount(compute_turnover_difference(i, turnover_projections, turnovers), trim=True, precision=5)|n}
                    </td>
                % endfor
                <td>
                    ${api.format_amount(turnovers['year_total'] - turnover_projections['year_total'], trim=True, precision=5)|n}
                </td>
            </tr>
            <tr><td>Pourcentage</td>
                % for i in range(1, 13):
                    <td id='gap_percent_${i}'>
                        ${compute_turnover_percent(i, turnover_projections, turnovers)}&nbsp;%
                    </td>
                % endfor
                <td>
                    ${compute_percent(turnovers['year_total'], turnover_projections['year_total'], 0)}&nbsp;%
                </td>
            </tr>
        </tbody>
    </table>
</div>
<div class='row'>
    <div class='col-md-6 col-md-offset-2 well' id="form_container">
        <a class="close" onclick="$('#form_container').fadeOut('slow');" title="Enlever">×</a>
        ${form.render()|n}
    </div>
</div>
</%block>
