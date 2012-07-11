# -*- coding: utf-8 -*-
    <div class='row estimationline' id="estimationline_${esc('id')}">
        <div class='span5'>
            <textarea class='span5' name="prestation_${esc('id')}">{{if prestation}}${esc('prestation')}{{/if}}</textarea>
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
            <button type='button' class='close' onclick="delRow('estimationline_${esc('id')}');">x</button>
        </div>
    </div>
