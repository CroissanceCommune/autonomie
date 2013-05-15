<%doc>
* Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
* Company : Majerti ( http://www.majerti.fr )

  This software is distributed under GPLV3
  License: http://www.gnu.org/licenses/gpl-3.0.txt
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
<div class='row'>
    <div class="span8 offset2" id="holidays"></div>
</div>
<div id="form-container" class='span4'>
</div>
<div id='messageboxes'>
</div>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${loadurl}";
</%block>
