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
        ${form.render()|n}
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
                    <td id='ca_prev_${i}'></td>
                % endfor
            </tr>
            <tr><td>CA réalisé</td>
                % for i in range(1, 13):
                    <td>${api.format_amount(realised_number[i])|n}</td>
                % endfor
            </tr>
            <tr><td>Écart</td>
                % for i in range(1, 13):
                    <td id='gap_${i}'></td>
                % endfor
            </tr>
            <tr><td>Pourcentage</td>
                % for i in range(1, 13):
                    <td id='gap_percent_${i}'></td>
                % endfor
            </tr>
        </tbody>
    </table>
</div>
</%block>
<%block name='footerjs'>
$('#year_form').find('select').change(function(){
    $('#year_form').submit();
    });
</%block>
