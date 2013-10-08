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

# -*- coding: utf-8 -*-
<div>
    <input type="hidden" name="__start__" value="${field.name}:sequence" class="deformProto" prototype="${field.widget.prototype(field)}">
    <div class='row linesblockheader'>
        % if field.schema.is_admin and field.schema.doctype is not 'estimation':
        <div class='span3'>Prestation</div>
        <div class='span1'>Prix/unité</div>
        <div class='span1'>Quantité</div>
        <div class='span2'>Unité</div>
        <div class='span1'>TVA</div>
        <div class='span2'>Code produit</div>
        % else:
            <div class='span4'>Prestation</div>
            <div class='span1'>Prix/unité</div>
            <div class='span1'>Quantité</div>
            <div class='span2'>Unité</div>
            <div class='span2'>TVA</div>
        % endif
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
            <button class='btn btn-mini btn-info pull-right' type="button" onclick='deform.appendSequenceItem($(this).parent().parent());cleanProductSelects();' id="${field.oid}-seqAdd">
                Ajouter une ligne
            </button>
        </div>
    </div>
    <input type="hidden" name="__end__" value="${field.name}:sequence"/>
</div>
