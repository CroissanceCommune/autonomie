<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%block name='headjs'>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.tmpl.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/estimation.js')}"></script>
</%block>
<%block name='content'>
Nom du devis:
<div class='row'>
    <div class='span3'>Prestation</div>
    <div class='span1'>Prix/unité</div>
    <div class='span1'>Quantité</div>
    <div class='span3'>Unité</div>
    <div class='span1'>Total</div>
</div>
<a href='#' onclick='addLine();'>
</a>
<div id='estimationcontainer'>
</div>
<text>$</text>{id}</text>
<script id="prestationTmpl" type="text/x-jquery-tmpl">
    <div class='row'>
        <div class='span3'>
            <textarea name="prestation_${esc('id')}"></textarea>
        </div>
        <div class='span1'>
            <input type='text' value='0' name="price_${esc('id')}" id="price_${esc('id')}"></input>
        </div>
        <div class='span1'>
            <input type='text' value='0' name="quantity_${esc('id')}" id="quantity_${esc('id')}"></input>
        </div>
        <div class='span3'>
            <select name="unity_${esc('id')}" id="unity_${esc('id')}">
                <option value='heure'>Heure</option>
                <option value='day'>Jour</option>
                <option value='week'>Semaine</option>
                <option value='forfait'>Forfait</option>
            </select>
        </div>
        <div class='span1'>
            <div id="total_${esc('id')}"></div>
        </div>
    </div>
</script>
</%block>
