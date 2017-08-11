/*
 * File Name : CheckboxWidget.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import $ from 'jquery';
import Mn from 'backbone.marionette';
import { getOpt } from "../tools.js";
import { updateSelectOptions } from '../tools.js';


var template = require('./templates/CheckboxWidget.mustache');

const CheckboxWidget = Mn.View.extend({
    template: template,
    ui:{
        checkbox: 'input[type=checkbox]'
    },
    events: {
        'click @ui.checkbox': 'onClick'
    },
    getCurrentValue: function(){
        var checked = this.getUI('checkbox').prop('checked');
        if (checked){
            return getOpt(this, 'true_val', '1');
        } else {
            return getOpt(this, 'false_val', '0');
        }
    },
    onClick: function(event){
        this.triggerMethod(
            'finish',
            this.getOption('field_name'),
            this.getCurrentValue(),
        );
    },
    templateContext: function(){
        var true_val = getOpt(this, 'true_val', '1');
        var checked = this.getOption('value') == true_val;
        return {
            title: this.getOption('title'),
            label: this.getOption('label'),
            description: this.getOption('description'),
            field_name: this.getOption('field_name'),
            checked: checked,
            editable: getOpt(this, 'editable', true)
        }
    }
});
export default CheckboxWidget;
