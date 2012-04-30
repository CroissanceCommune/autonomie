<%doc>
    Template for estimation edition/creation
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%namespace file="/base/utils.mako" import="address"/>
<%block name='headjs'>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.tmpl.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/estimation.js')}"></script>
</%block>
<%block name='css'>
<link href="${request.static_url('autonomie:static/css/estimation.css')}" rel="stylesheet"  type="text/css" />
</%block>
<%block name='content'>
<div class="container">
    <dl class="dl-horizontal">
        <dt>Prestataire</dt>
        <dd>${address(company, 'company')}</dd>
        <dt>Client</dt>
        <dd>${address(client, 'client')}</dd>
        </dl>
${html_form|n}
</%block>
<%block name='footerjs'>
initialize();
</%block>
