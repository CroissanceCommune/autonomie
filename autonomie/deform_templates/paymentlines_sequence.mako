# -*- coding: utf-8 -*-
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
    Payments table
    Uses jquery tmpl to generate the lines
</%doc>
<% import colander %>
<%def name='esc(datas)'><%text>${</%text>${datas}<%text>}</%text>\
</%def>
<div>
    <input type="hidden" name="__start__" value="${field.name}:sequence"/>
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
                <input type="hidden" name="__start__" value="paymentDate:mapping"></input>
                <input class='input-mini' type='text' id="paymentDate_${esc('id')}" name="displayDate" {{if paymentDate}}value="${esc('paymentDate')}"{{/if}}></input>
                <input class='input-mini' type='hidden' id="paymentDate_${esc('id')}_altField" name="date" {{if paymentDate}}value="${esc('paymentDate')}"{{/if}}></input>
                {{if paymentDate_error}}
                <span class='help-inline'>
                    <span class='error'>${esc('paymentDate_error')}</span>
                </span>
                {{/if}}
                <input type="hidden" name="__end__" value="paymentDate:mapping"></input>
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
                <input class='input-mini' type='text' name="amount" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0,00 €{{/if}}"></input>
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
                <button type='button' class='close' onclick="delRow('paymentline_${esc('id')}');">x</button>
            </div>
            {{/if}}
            <input type="hidden" name="__end__" value="${field.name}:mapping"/>
        </div>
    </script>
    <script id="paymentAmountTmpl" type="text/x-jquery-tmpl">
        <div class='span2 control-group offset2 paymentamount {{if amount_error}}control-group error{{/if}}'>
            <input class='input-mini' type='text' name="amount" id="amount_${esc('id')}" value="{{if amount}}${esc('amount')}{{else}}0,00 €{{/if}}"></input>
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
            <button type='button' class='close' onclick="delRow('paymentline_${esc('id')}');">x</button>
        </div>
    </script>
    <div class='row linesblockheader'>
        <div class='span5'>Libellé</div>
        <div class='span2'>Date</div>
        <div class='span2 offset2 paymentamount'>Montant</div>
    </div>
    <div id='account_container' style='display:none;'>
        <div class='span5' style="margin-left:0px;">Facture d'acompte</div>
        <div class='span2'>À la commande</div>
        <div class='span2 offset2 paymentamount' id='account_amount'><div class='input'>0,00 €</div></div>
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
        else:
            for key, value in solde.items():
                if value == colander.null:
                    solde.pop(key)
        if not isinstance(solde.get('paymentDate', '0'), basestring):
            solde['paymentDate'] = '';
    %>
    <script type='text/javascript'>
        var description = "";
        % for line in solde.get('description', "Solde").splitlines():
            description += "${line}";
            % if not loop.last:
                description += "\n";
            % endif
        % endfor
        var solde = {amount:formatAmount("${solde.get('amount', '0')}"),
            description:description,
            paymentDate:"${solde.get('paymentDate')}",
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

            % if isinstance(sub[0], dict):
                % if not isinstance(sub[0].get('amount', '0'), basestring):
                    <%
                        sub[0]['amount'] = " ";
                    %>
                % endif
                % if not isinstance(sub[0].get('paymentDate', '0'), basestring):
                    <%
                        sub[0]['paymentDate'] = " ";
                    %>
                %endif
                var description = "";
                % for description_line in sub[0].get('description', "Paiement").splitlines():
                    description += "${description_line}\n";
                % endfor

                var line = {amount:formatAmount("${sub[0].get('amount', '0')}"),
                    description:description,
                    paymentDate:"${sub[0].get('paymentDate', '')}",
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
