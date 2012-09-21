# -*- coding: utf-8 -*-
<div>
    <div class='control-group estimationamounts offset8' id='tasklines_ht'>
        <div class='control-label'>
            Total HT avant remise
        </div>
        <div class='controls'>
            <div class='input'></div>
        </div>
    </div>
    <input type="hidden" name="__start__" value="${field.name}:sequence" class="deformProto" prototype="${field.widget.prototype(field)}">
    <div id="discount_header" class='row linesblockheader' style='display:none;visible:false;'>
        <div class='span4'>Remise</div>
        <div class='span1'>Montant</div>
        <div class='span2 offset3'>TVA</div>
        <div class='span1'>Total HT</div>
    </div>
    <div class="deformSeqContainer">

        % for sub in subfields:
            ${field.renderer(field.widget.item_template, field=sub[1], cstruct=sub[0], parent=field)|n}
        % endfor
        <%
            min_len = field.widget.min_len
            max_len = field.widget.max_len
            now_len = len(subfields)
        %>

        <span class="deformInsertBefore" min_len="${min_len}" max_len="${max_len}" now_len="${now_len}"></span>
    </div>
    <div class='row'>
        <div class='span2 offset10'>
            <button class='btn btn-mini btn-info pull-right' type="button" onclick='$("#discount_header").show();deform.appendSequenceItem($(this).parent().parent());' id="${field.oid}-seqAdd">
                Ajouter une remise
            </button>
        </div>
    </div>
    <input type="hidden" name="__end__" value="${field.name}:sequence"/>
</div>
