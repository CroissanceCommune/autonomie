<%doc>
    Payments table
    Uses jquery tmpl to generate the lines
</%doc>
<%namespace file="/base/utils.mako" import="esc"/>
<div>
    <input type="hidden" name="__start__" value="${field.name}:sequence">
    <script id="paymentTmpl" type="text/x-jquery-tmpl">
        <input type="hidden" name="__start__" value="${field.name}:mapping"/>
        <div class='row paymentline' id="paymentline_${esc('id')}">
            <div class='span5'>
                <textarea class='span5' name="description">{{if description}}${esc('description')}{{else}}Livrable{{/if}}</textarea>
            </div>
            <div class='span2' id="date_${esc('id')}">
                <input class='input-mini' type='text' id="paymentDate_${esc('id')}" name="paymentDate" {{if date}}value="${esc('date')}"{{/if}}></input>
            </div>
            {{if readonly}}
            <div class='span2 offset2 paymentamount'>
                <div class='input'>{{if amount}}${esc('amount')}{{/if}}</div>
            </div>
            {{else}}
            <div class='span2 offset2 paymentamount'>
                <input class='input-mini' type='text' name="amount" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0{{/if}}"></input>
                <button class='btn btn-mini btn-info pull-right' type="button" onclick='addPaymentRow({readonly:false, description:"Paiement"}, "#paymentline_${esc('id')}");'>
                    + Ajouter une échéance
                </button>
            </div>
            <div class='span1'>
                <button type='button' class='close' onclick="delRow('paymentline_${esc('id')}');">x</a>
            </div>
            {{/if}}
        </div>
        <input type="hidden" name="__end__" value="${field.name}:mapping"/>
    </script>
    <script id="paymentAmountTmpl" type="text/x-jquery-tmpl">
        <input class='input-mini' type='text' name="amount" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0{{/if}}"></input>
        <button class='btn btn-mini btn-info pull-right' type="button" onclick='addPaymentRow({readonly:false, description:"Paiement"}, "#paymentline_${esc('id')}");'>
        + Ajouter une échéance
        </button>
    </script>

    <div class='row linesblockheader'>
        <div class='span5'>Libellé</div>
        <div class='span2'>Date</div>
        <div class='span2 offset2'>Montant</div>
    </div>
    <div id='account_container' style='display:none;'>
        <div class='span5' style="margin-left:0px;">Facture d'accompte</div>
        <div class='span2'>À la commande</div>
        <div class='span2 offset2' id='account_amount'><div class='input'>0</div></div>
    </div>
    <div id='paymentcontainer'></div>
    <%doc>
        Here we get the last payment row which should be the sold
        We then add a row after paymentcontainer since this one should never be removable
    </%doc>
    <%
        solde = subfields[-1]
        if not isinstance(solde, dict):
            solde = {}
    %>
    <script type='text/javascript'>
        var solde = ${solde};
        // the sold line should not be editable anyway
        solde['readonly'] = true;
        solde['id'] = 1000;
        if (solde['description'] === undefined){
            solde['description'] = "Solde";
        }
        addPaymentRow(solde, '#paymentcontainer');
    </script>
    <script type='text/javascript'>
        ## We go through the rest of the rows to add payment rows
        ## We have to check if their editable or not when adding them
        % for sub in subfields[:-1]:
            % if isinstance(sub[0], dict):
                addPaymentRow(${sub[0]});
            % endif
        % endfor
        $('select[name=deposit]').change(function(){
            $(Facade).trigger('depositchange', this);
        });
        $('select[name=payment_times]').change(function(){
            $(Facade).trigger('payment_timeschange', this);
        });
    </script>
    <input type="hidden" name="__end__" value="${field.name}:sequence"/>
</div>
