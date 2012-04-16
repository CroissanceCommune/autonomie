# -*- coding: utf-8 -*-
<%doc>
    Payments table
    Uses jquery tmpl to generate the lines
</%doc>
<%def name='esc(datas)'><%text>${</%text>${datas}<%text>}</%text>\
</%def>
<div>
    <input type="hidden" name="__start__" value="${field.name}:sequence">
    <script id="paymentTmpl" type="text/x-jquery-tmpl">
        <div class='row paymentline' id="paymentline_${esc('id')}">
            <input type="hidden" name="__start__" value="${field.name}:mapping"/>
            <div class='span5 control-group {{if description_error}}error{{/if}}'>
                <textarea class='span5' name="description">{{if description}}${esc('description')}{{else}}Livrable{{/if}}</textarea>
                {{if description_error}}
                <span class='help-inline'>
                    <span class='error'>${esc('description_error')}</span>
                </span>
                {{/if}}
            </div>
            <div class='span2 control-group {{if paymentDate_error}}error{{/if}}' id="date_${esc('id')}">
                <input class='input-mini' type='text' id="paymentDate_${esc('id')}" name="paymentDate" {{if date}}value="${esc('date')}"{{/if}}></input>
                {{if paymentDate_error}}
                <span class='help-inline'>
                    <span class='error'>${esc('paymentDate_error')}</span>
                </span>
                {{/if}}
            </div>
            {{if readonly}}
            <div class='span2 offset2 paymentamount {{if amount_error}}control-group error{{/if}}'>
                <div class='input'>{{if amount}}${esc('amount')}{{/if}}</div>
                <input type='hidden' value="{{if amount}}${esc('amount')}{{/if}}" name="amount"></input>
                {{if amount_error}}
                <span class='help-inline'>
                    <span class='error'>${esc('amount_error')}</span>
                </span>
                {{/if}}
            </div>
            {{else}}
            <div class='span2 control-group offset2 paymentamount {{if amount_error}}control-group error{{/if}}'>
                <input class='input-mini' type='text' name="amount" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0{{/if}}"></input>
                <button class='btn btn-mini btn-info pull-right' type="button" onclick='addPaymentRow({readonly:false, description:"Paiement"}, "#paymentline_${esc('id')}");'>
                    + Ajouter une échéance
                </button>
                {{if amount_error}}
                <span class='help-inline'>
                    <span class='error'>${esc('amount_error')}</span>
                </span>
                {{/if}}
            </div>
            <div class='span1'>
                <button type='button' class='close' onclick="delRow('paymentline_${esc('id')}');">x</a>
            </div>
            {{/if}}
            <input type="hidden" name="__end__" value="${field.name}:mapping"/>
        </div>
    </script>
    <script id="paymentAmountTmpl" type="text/x-jquery-tmpl">
        <div class='span2 control-group offset2 paymentamount {{if amount_error}}control-group error{{/if}}'>
            <input class='input-mini' type='text' name="amount" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0{{/if}}"></input>
            <button class='btn btn-mini btn-info pull-right' type="button" onclick='addPaymentRow({readonly:false, description:"Paiement"}, "#paymentline_${esc('id')}");'>
                + Ajouter une échéance
            </button>
            {{if amount_error}}
            <span class='help-inline'>
                <span class='error'>${esc('amount_error')}</span>
            </span>
            {{/if}}
        </div>
        <div class='span1'>
            <button type='button' class='close' onclick="delRow('paymentline_${esc('id')}');">x</a>
        </div>
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
        solde, soldefield = subfields[-1]
        if not isinstance(solde, dict):
            solde = {}
    %>
    <script type='text/javascript'>
        "${solde}";
        var solde = {amount:"${solde.get('amount', '0')}",
            description:"${solde.get('description', "Solde")}",
            readonly:true,
            id:1000};
        % if soldefield.error:
            % for key, value in soldefield.error.asdict().items():
                solde["${key[2:]}_error"] = "${_(value)}";
            % endfor
        % endif
        addPaymentRow(solde, '#paymentcontainer');
    </script>
    <script type='text/javascript'>
        ## We go through the rest of the rows to add payment rows
        ## We have to check if their editable or not when adding them
        % for sub in subfields[:-1]:
            "${sub[1].error.asdict()}";

            % if isinstance(sub[0], dict):
                % if not isinstance(sub[0].get('amount', '0'), str):
                    <%
                        sub[0]['amount'] = " ";
                    %>
                % endif
                var line = {amount:"${sub[0].get('amount', '0')}",
                    description:"${sub[0].get('description', "Paiement")}",
                    readonly:true};
                % if sub[1].error:
                    % for key, value in sub[1].error.asdict().items():
                        line["${key[2:]}_error"] = "${_(value)}";
                    % endfor
                % endif
                addPaymentRow(line);
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
