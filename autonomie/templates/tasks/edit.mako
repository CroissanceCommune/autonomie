<%doc>
    Template for estimation and invoice edition/creation
</%doc>
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%namespace file="/base/utils.mako" import="address"/>
<%block name='css'>
<link href="${request.static_url('autonomie:static/css/task.css')}" rel="stylesheet"  type="text/css" />
</%block>
<%block name='content'>
    <dl class="dl-horizontal">
        <dt>Prestataire</dt>
        <dd>${address(company, 'company')}</dd>
        </dl>
${form|n}
</%block>
<%block name='footerjs'>
initialize();
</%block>
