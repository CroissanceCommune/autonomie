<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
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
Main job page
should load dynamically the datas about a job execution
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name="content">
<div class="row">
    <div class="col-md-8 col-md-offset-2" id="ajax_container">
    </div>
</div>
<script type='text/javascript'>
    AppOptions['url'] = "${url}";
    AppOptions['dataType'] = "${request.context.type_}"
</script>
</%block>
