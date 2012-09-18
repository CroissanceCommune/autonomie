<%doc>
Page de tests javascript
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name='headjs'>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.tmpl.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/task.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/tests/qunit.js')}"></script>
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
