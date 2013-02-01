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
</div>
</%block>
