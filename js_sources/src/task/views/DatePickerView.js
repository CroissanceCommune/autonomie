/*
 * File Name : DatePickerView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import Mn from 'backbone.marionette';
import { getOpt, setDatePicker } from '../../tools.js';


var template = require('./templates/widgets/DatePickerView.mustache');

const DatePickerView = Mn.View.extend({
    template: template,
    ui: {
        altdate: "input[name=altdate]" ,
    },
    onDateSelect: function(){
        /* On date select trigger a change event */
        const value = $(this.getSelector()).val();
        this.triggerMethod('change', this.getOption('field_name'), value);
    },
    getSelector: function(){
        /* Return the selector for the date input */
        return "input[name=" + getOpt(this, 'field_name', 'date') + "]";
    },
    onAttach: function(){
        /* On attachement in case of edit, we setup the datepicker */
        if (getOpt(this, 'editable', true)){
            let date = this.getOption('date');
            let selector = this.getSelector();
            setDatePicker(
                this.getUI('altdate'),
                selector,
                date,
                // Bind the method to access view through the 'this' param
                {onSelect: this.onDateSelect.bind(this)}
            );
        }
    },
    templateContext: function(){
        /*
         * Give parameters for the templating context
         */
        let ctx = {
            editable: getOpt(this, 'editable', true),
            title: getOpt(this, 'title', 'Date'),
            description: getOpt(this, 'description', ''),
            field_name: getOpt(this, 'field_name', 'date'),
        };
        if (!getOpt(this, 'editable', true)){
            ctx['date'] = formatDate(this.getOption('date'));
        }
        return ctx;
    }
});
export default DatePickerView;
