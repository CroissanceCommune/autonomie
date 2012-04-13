<%doc>
    Template for estimation edition/creation
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%namespace file="/base/utils.mako" import="address"/>
<%def name='Row(label, tagid, formtag=None)'>
    <div class='control-group'>
        <div class='control-label'>
            ${label}
        </div>
        <div id='${tagid}' class='controls'>
            % if formtag != None:
                ${formtag|n}
            % else:
                <div class='input'></div>
            % endif
        </div>
    </div>
</%def>
<%block name='headjs'>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.tmpl.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/estimation.js')}"></script>
</%block>
<%block name='css'>
<link href="${request.static_url('autonomie:static/css/estimation.css')}" rel="stylesheet"  type="text/css" />
</%block>
<%block name='content'>
<div class="container">
${form|n}
</%block>
<%block name='footerjs'>
initialize();
</%block>
