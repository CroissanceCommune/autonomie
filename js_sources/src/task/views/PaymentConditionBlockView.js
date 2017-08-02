/*
 * File Name : PaymentConditionBlockView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import SelectWidget from './SelectWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import {getDefaultItem} from '../../tools.js';
import FormBehavior from '../behaviors/FormBehavior.js';

var template = require("./templates/PaymentConditionBlockView.mustache");

const PaymentConditionBlockView = Mn.View.extend({
    behaviors: [FormBehavior],
    tagName: 'div',
    className: 'form-section',
    template: template,
    regions: {
        predefined_conditions: '.predefined-conditions',
        conditions: '.conditions',
    },
    modelEvents: {
        'change:payment_conditions': 'render'
    },
    childViewEvents: {
        'finish': 'onFinish',
    },
    initialize: function(){
        this.lookupDefault();
    },
    onFinish(field_name, value){
        if (field_name == 'predefined_conditions'){
            var condition_object = this.getCondition(value);

            this.model.set('predefined_conditions', value);
            if (!_.isUndefined(condition_object)){
                this.triggerMethod('data:persist', 'payment_conditions', condition_object.label);
            }
        } else {
            this.triggerMethod('data:persist', 'payment_conditions', value);
        }
    },
    getCondition(id){
        return _.find(
            AppOption['form_options']['payment_conditions'],
            function(item){ return item.id == id;}
        );
    },
    lookupDefault(){
        /*
         * Setup the default payment condition if none is set
         */
        var option = getDefaultItem(
            AppOption['form_options']['payment_conditions']
        );
        if (!_.isUndefined(option)){
            if (!this.model.get('payment_conditions')){
                this.model.set('payment_conditions', option.label);
            }
        }
    },
    onRender: function(){
        var val = this.model.get('predefined_conditions');
        val = parseInt(val, 10);
        this.showChildView(
            'predefined_conditions',
            new SelectWidget(
                {
                    options: AppOption['form_options']['payment_conditions'],
                    title: "",
                    field_name: 'predefined_conditions',
                    id_key: 'id',
                    value: val,
                    add_default: true
                }
            )
        );
        this.showChildView(
            'conditions',
            new TextAreaWidget(
                {
                    value: this.model.get('payment_conditions'),
                    placeholder: "Conditions de paiement applicables à ce document",
                    field_name: 'payment_conditions',
                }
            )
        );
    }
});
export default PaymentConditionBlockView;
