<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%block name='headjs'>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.tmpl.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('autonomie:static/js/estimation.js')}"></script>
</%block>
<%block name='content'>
<form name='estimation' method='POST' class='form-inline'>
Nom du devis:
<div class='row'>
    <div class='span6'>Prestation</div>
    <div class='span1'>Prix/unité</div>
    <div class='span1'>Quantité</div>
    <div class='span2'>Unité</div>
    <div class='span1 offset1'>Total</div>
</div>
<div id='estimationcontainer'>
</div>
<a class='btn' href='#' onclick='addLine();'>
    Ajouter une ligne
</a>
<div class='row'>
    <div class='span6'>
        Total HT avant Remise
    </div>
    <div id='linestotal' class='span1 offset5'>
        <input type='text' value='0' class='input-mini'></input>
    </div>
</div>
<div class='row'>
    <div class='span6'>
        Remise
    </div>
    <div id='discount' class='span1 offset5'>
        <input name='discount' value='0' class='input-mini'> </input>
    </div>
</div>
<div class='row'>
    <div class='span6'>
        Total HT
    </div>
    <div id='httotal' class='span1 offset5'>
        <input type='text' value='0' class='input-mini'></input>
    </div>
</div>
<div class='row'>
    <div class='span6'>
        TVA à appliquer
    </div>
    <div id='tva' class='span1 offset5'>
        <select name='tva' class='span1'>
            <option value='500'>5%</option>
            <option value='1960'>19.6%</option>
        </select>
    </div>
</div>
<div class='row'>
    <div class='span6'>
        Montant TVA
    </div>
    <div id='tvapart' class='span1 offset5'>
        <input type='text' value='0' class='input-mini'></input>
    </div>
</div>
<div class='row'>
    <div class='span6'>
        Frais liés à la prestation
    </div>
    <div id='expenses' class='span1 offset5'>
        <input name='expenses' type='text' class='input-mini'></input>
    </div>
</div>
<div class='row'>
    <div class='span6'>
        Total TTC
    </div>
    <div id='total' class='span1 offset5'>
        <input type='text' value='0' class='input-mini'></input>
    </div>
</div>
<input type='submit'></input>
</form>
<script id="prestationTmpl" type="text/x-jquery-tmpl">
    <div class='row estimation_line' id="estimation_line_${esc('id')}">
        <div class='span6'>
            <textarea name="prestation_${esc('id')}"></textarea>
        </div>
        <div class='span1' id="price_${esc('id')}">
            <input class='input-mini' type='text' value='0' name="price_${esc('id')}"></input>
        </div>
        <div class='span1' id="quantity_${esc('id')}">
            <input class='input-mini' type='text' value='0' name="quantity_${esc('id')}"></input>
        </div>
        <div class='span2'>
            <select class='span2' name="unity_${esc('id')}" id="unity_${esc('id')}">
                <option value='heure'>Heure</option>
                <option value='day'>Jour</option>
                <option value='week'>Semaine</option>
                <option value='forfait'>Forfait</option>
            </select>
        </div>
        <div class='span1 offset1' id="total_${esc('id')}">
            <input type='text' value='0' class='input-mini'></input>
        </div>
    </div>
</script>
</%block>
<%block name='footerjs'>
$(function(){
    setDefault();
});
</%block>
