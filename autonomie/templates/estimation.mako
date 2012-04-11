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
<%block name='content'>
<style>
    .estimationform{
        margin-left:50px;
    }
    .input{
    padding:6px 1px;
    margin:1px;
    }
    .estimation_line{
    margin-bottom:5px;
    padding-bottom:2px;
    padding-top:2px;
    border-bottom:1px solid #dddddd;
    }
    .estimationlinesheader{
    background-color:#f2f2f2;
    margin-bottom:10px;
    font-weight:bold;
    }
    .estimationamounts{
    padding-left:640px;
    }
    .estimationform .control-group{
    margin-bottom:2px;
    }
    .estimationlines{
        width:940px;
        margin-left:160px;
    }
    .paymentamount{
        text-align:right;
    }
</style>
<form name='estimation' method='POST' class='form-horizontal estimationform'>
    <%
        phase_options = ""
        for phase in phases:
            phase_options += "<option value='%s'>%s</option>" % (phase.id, phase.name)
            phase_select = "<select>" + phase_options + "</select>"
    %>
    ${Row(u"Phase", "", phase_select)}
    ${Row(u"De ", "", capture(address, company, 'company'))}
    ${Row(u"Pour", "", capture(address, client, 'client'))}
    ${Row(u"Date du devis", "", "<input name='taskDate' id='taskDate' type='text'></input>")}
    ${Row(u"Numéro du devis", "", "DDDD_DDDD")}
    ${Row(u"Objet de la prestation", "", "<textarea name='description' class='span10'></textarea>")}
    ${Row(u"Formation", "", "<input type='checkbox' name='course' 'value='1'></input>")}
    ${Row(u"Affichage des unités", "", "<input type='checkbox' name='displayedUnits' value='1'></input>")}
    <div class='estimationlines'>
    <div class='label'>Détail de la prestation</div>
    <div class='row estimationlinesheader'>
        <div class='span5'>Prestation</div>
        <div class='span1'>Prix/unité</div>
        <div class='span1'>Quantité</div>
        <div class='span2'>Unité</div>
        <div class='span1 offset1'>Total</div>
    </div>
    <div id='estimationcontainer'>
    </div>
    <div class='row'>
        <button class='btn btn-mini btn-info pull-right' type="button" onclick='addEstimationRow();'>
        Ajouter une ligne
        </button>
    </div>
    <div class='estimationamounts'>
    ${Row(u"Total HT avant Remise", "linestotal")}
    ${Row(u"Remise", 'discount', "<input name='discount' value='0' class='input-mini'> </input>")}
    ${Row(u"Total HT", "httotal")}
    ${Row(u"TVA à appliquer", "tva", "<select name='tva' class='span2'><option value='500'>5%</option><option value='1960'>19.6%</option></select>")}
    ${Row(u"Montant TVA", 'tvapart')}
    ${Row(u"Frais liés à la prestation", 'expenses', "<input name='expenses' type='text' value='0' class='input-mini'></input>")}
    ${Row(u"Total TTC", "total")}
    </div>
</div>
${Row(u"Notes", "", "<textarea name='exclusions' class='span10'></textarea>")}
<div class='estimationlines'>
    <div class='label'>Conditions de paiement</div>
<%
    percent_options = "<option value='0' default='true'>0 %</option><option value='5' default='true'>5 %</option>"
    for val in range(10,100,10):
        percent_options += "<option value='%s'>%s %%</option>" % (val,val)
    percent_select = "<select>" + percent_options + "</select>"
%>
${Row(u"Accompte à la commande", "account_percent", percent_select)}
<%
nbpayment_options = "<option value='-1'>manuel</option>"
for val in range(1, 12):
    nbpayment_options += "<option value='%s'>%s fois</option>" % (val,val)
nbpayment_select = "<select>" + nbpayment_options + "</select>"
%>
${Row(u"Nombre de paiement", "nbpayment", nbpayment_select)}
<%
    options = ((u'Les paiments ne sont pas affichés dans le PDF.', "NONE",), (u"Le résumé des paiements apparaissent dans le PDF.", "SUMMARY",), (u"Le détail des paiements apparaît dans le PDF.", "ALL",),)
    radios = ""
    for label, value in options:
        radios +="<label class='radio'><input type='radio' name='paymentDisplay' value='%s'></input>%s</label>" % (value, label,)

%>
${Row(u"Affichage des paiements", "", radios)}

    <div class='row estimationlinesheader'>
        <div class='span5'>Libellé</div>
        <div class='span2'>Date</div>
        <div class='span2 offset2'>Montant</div>
    </div>
    <div id='account_container' style='display:none;'>
        <div class='span5' style="margin-left:0px;">Facture d'accompte</div>
        <div class='span2'>À la commande</div>
        <div class='span2 offset2' id='account_amount'><div class='input'>0</div></div>
    </div>
    <div id='paymentcontainer'>

    </div>
</div>

<div class='form-actions'>
    <input class="btn btn-primary"  type='submit'></input>
</div>
</form>
<script id="prestationTmpl" type="text/x-jquery-tmpl">
    <div class='row estimation_line' id="estimation_line_${esc('id')}">
        <div class='span5'>
            <textarea class='span5' name="prestation_${esc('id')}">
                {{if prestation}}
                ${esc('prestation')}
                {{/if}}
            </textarea>
        </div>
        <div class='span1' id="price_${esc('id')}">
            <input class='input-mini' type='text' name="price_${esc('id')}" {{if price}}value="${esc('price')}"{{else}}value="0"{{/if}}></input>
        </div>
        <div class='span1' id="quantity_${esc('id')}">
            <input class='input-mini' type='text' name="quantity_${esc('id')}" {{if quantity}}value="${esc('quantity')}"{{else}}value="0"{{/if}}></input>
        </div>
        <div class='span2'>
            <select class='span2' name="unity_${esc('id')}" id="unity_${esc('id')}">
                <option value='NONE'  {{if unity}}{{if unity=='NONE'}}selected='true'{{/if}}{{/if}} >-</option>
                <option value='HOUR'  {{if unity}}{{if unity=='HOUR'}}selected='true'{{/if}}{{/if}}>Heure(s)</option>
                <option value='DAY'   {{if unity}}{{if unity=='DAY'}}selected='true'{{/if}}{{/if}}>Jour(s)</option>
                <option value='WEEK'  {{if unity}}{{if unity=='WEEK'}}selected='true'{{/if}}{{/if}}>Semaine(s)</option>
                <option value='MONTH' {{if unity}}{{if unity=='MONTH'}}selected='true'{{/if}}{{/if}}>Mois</option>
                <option value="FEUIL" {{if unity}}{{if unity=='FEUIL'}}selected='true'{{/if}}{{/if}}>Feuillet(s)</option>
                <option value='PACK'  {{if unity}}{{if unity=='PACK'}}selected='true'{{/if}}{{/if}}>Forfait</option>
            </select>
        </div>
        <div class='span1 offset1 linetotal' id="total_${esc('id')}">
            <div class='input'></div>
        </div>
        <div class='span1'>
            <button type='button' class='close' onclick="delRow('estimation_line_${esc('id')}');">x</a>
        </div>
    </div>
</script>
<script id="paymentTmpl" type="text/x-jquery-tmpl">
    <div class='row paymentline' id="paymentline_${esc('id')}">
        <div class='span5'>
            <textarea class='span5' name="description_${esc('id')}">{{if description}}${esc('description')}{{else}}Livrable{{/if}}</textarea>
        </div>
        <div class='span2' id="date_${esc('id')}">
            <input class='input-mini' type='text' id="paymentDate_${esc('id')}" name="paymentDate_${esc('id')}" {{if date}}value="${esc('date')}"{{/if}}></input>
            </div>
            {{if readonly}}
            <div class='span2 offset2 paymentamount'>
                <div class='input'>{{if amount}}${esc('amount')}{{/if}}</div>
            </div>
                    {{else}}
            <div class='span2 offset2 paymentamount'>
                    <input class='input-mini' type='text' name="amount_${esc('id')}" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0{{/if}}"></input>
                    <button class='btn btn-mini btn-info pull-right' type="button" onclick='addPaymentRow({readonly:false, description:"Paiement"}, "#paymentline_${esc('id')}");'>
                    + Ajouter une échéance
                    </button>
            </div>
            <div class='span1'>
                <button type='button' class='close' onclick="delRow('paymentline_${esc('id')}');">x</a>
            </div>
                    {{/if}}
        </div>

    </div>
</script>
</%block>
<%block name='footerjs'>
$(function(){
    setDefault();
});
</%block>
