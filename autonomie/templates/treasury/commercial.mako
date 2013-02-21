<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
  Commercial handling page
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name='content'>
<div class='row'>
<div class='span8 offset2'>
<table class='table table-striped table-bordered' style="margin-top:15px">
<tr><td><b>Nombre de devis rédigés</b></td><td><b>${estimations}</b></td></tr>
<tr><td><b>Nombre de devis concrétisés</b></td><td><b>${validated_estimations}</b></td></tr>
<tr><td><b>Nombre de client</b></td><td><b>${clients}</b></td></tr>
</table>
</div>
</div>
<div class='row'>
    <div class='span2 offset8'>
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
        </thead>
        <tbody>
            <tr><td>CA prévisionnel</td>
                % for i in range(1, 13):
                    <% turnover = turnover_projections.get(i) %>
                        % if turnover:
                            <td id='ca_prev_${i}' title='${turnover.comment}'>
                                 ${api.format_amount(turnover.value)|n}
                        % else:
                            <td id='ca_prev_${i}'>
                        % endif
                        <a href='#setform'
                            % if turnover:
                                title='${turnover.comment}' onclick='setTurnoverProjectionForm("${i}", "${turnover.value/100.0}", this);'>
                            % else:
                                onclick='setTurnoverProjectionForm("${i}");'>
                            % endif
                            <i class="icon icon-pencil"></i>
                        </a>
                    </td>
                % endfor
            </tr>
            <tr><td>CA réalisé</td>
                % for i in range(1, 13):
                    <td>${api.format_amount(turnovers[i])|n}</td>
                % endfor
            </tr>
            <tr><td>Écart</td>
                % for i in range(1, 13):
                    <td id='gap_${i}'>
                        ${api.format_amount(compute_difference(i, turnover_projections, turnovers))|n}
                    </td>
                % endfor
            </tr>
            <tr><td>Pourcentage</td>
                % for i in range(1, 13):
                    <td id='gap_percent_${i}'>
                        ${api.format_amount(compute_percent(i, turnover_projections, turnovers)*100)}&nbsp;%
                    </td>
                % endfor
            </tr>
        </tbody>
    </table>
</div>
<div class='row'>
    <div class='span6 offset2 well' id="form_container">
        <a class="close" onclick="$('#form_container').fadeOut('slow');" title="Enlever">×</a>
        ${form.render()|n}
    </div>
</div>
</%block>
