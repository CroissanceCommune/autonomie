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
Page de tests javascript
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name='headjs'>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/tests/test_math.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/tests/test_dom.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/tests/test_date.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/tests/test_task.js')}"></script>
</%block>
<%block name='css'>
<link rel="stylesheet" href="${request.static_url('autonomie:static/js/tests/qunit.css')}" />
</%block>
<%block name='content'>
<h1 id="qunit-header">${title}</h1>
<h2 id="qunit-banner"></h2>
<div id="qunit-testrunner-toolbar"></div>
<h2 id="qunit-userAgent"></h2>
<ol id="qunit-tests"></ol>
<div id="qunit-fixture"></div>
</div>
</%block>
