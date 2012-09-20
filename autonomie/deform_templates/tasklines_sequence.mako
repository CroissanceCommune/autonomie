# -*- coding: utf-8 -*-
<div>
    <input type="hidden" name="__start__" value="${field.name}:sequence" class="deformProto" prototype="${field.widget.prototype(field)}">
    <div class='row linesblockheader'>
        <div class='span4'>Prestation</div>
        <div class='span1'>Prix/unité</div>
        <div class='span1'>Quantité</div>
        <div class='span2'>Unité</div>
        <div class='span2'>TVA</div>
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
            <button class='btn btn-mini btn-info pull-right' type="button" onclick='deform.appendSequenceItem($(this).parent().parent());' id="${field.oid}-seqAdd">
                Ajouter une ligne
            </button>
        </div>
    </div>
    <input type="hidden" name="__end__" value="${field.name}:sequence"/>
    <div class='control-group estimationamounts offset8' id='tasklines_ht'>
        <div class='control-label'>
            Total HT avant remise
        </div>
        <div class='controls'>
            <div class='input'></div>
        </div>
    </div>
</div>
