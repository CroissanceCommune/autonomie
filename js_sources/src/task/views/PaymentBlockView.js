/*
 * File Name : PaymentBlockView.js
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
import {findCurrentSelected} from '../../tools.js';
import FormBehavior from '../behaviors/FormBehavior.js';
import PaymentLineTableView from './PaymentLineTableView.js';

var template = require("./templates/PaymentBlockView.mustache");

const PaymentBlockView = Mn.View.extend({
    behaviors: [FormBehavior],
    tagName: 'div',
    className: 'form-section',
    template: template,
    regions: {
        payment_display: '.payment_display-container',
        payment_times: '.payment_times-container',
        deposit: '.payment-deposit-container',
        lines: '.payment-lines-container',
    },
    modelEvents: {
//        'change:payment_conditions': 'render'
    },
    childViewEvents: {
        'finish': 'onFinish',
    },
    initialize: function(options){
        this.collection = options['collection'];
    },
    onFinish(field_name, value){
        /*
         * Launch when a field has been modified
         *
         * Handles fields that impact the payment lines
         *
         *      payment_times
         *
         *              we generate the payment lines
         *
         *      paymentDisplay
         *
         *              we hide/show the date field
         *
         */
        if (field_name == 'paymentDisplay'){
            var old_value = this.model.get('paymentDisplay');
            this.triggerMethod('data:persist', 'paymentDisplay', value);
            // If it changed and it is or was ALL_NO_DATE we render the lines again
            if ((old_value != value) && _.indexOf([value, old_value], 'ALL_NO_DATE') != -1){
                this.renderTable();
            }
        } else if (field_name == 'payment_times'){
            var old_value = this.model.get('payment_times');
            if (old_value != value){
                if (value != -1){
                    // We generate the payment lines (and delete old ones)
                    var this_ = this;
                    var deferred = this.collection.genPaymentLines(value);

                    // We set the datas after because setting it, we also sync
                    // the model and payment_times attribute is compuated based
                    // on the lines that are added/deleted in the given
                    // deferred
                    deferred.then(function(){
                        this_.triggerMethod('data:persist', field_name, value);
                    });
                 } else {
                     this.triggerMethod('data:persist', field_name, value);
                 }
                if ((value == -1) || (old_value == -1)){
                    // If we set it on manual configuration we re-render the
                    // table
                    this.renderTable();
                }
            }
        }
    },
    renderTable: function(){
        var edit = false;
        if (this.model.get('payment_times') == -1){
            edit = true;
        }
        var show_date = true;
        if (this.model.get('paymentDisplay') == 'ALL_NO_DATE'){
            show_date = false;
        }
        this.showChildView(
            'lines',
            new PaymentLineTableView({
                collection: this.collection,
                model: this.model,
                edit: edit,
                show_date: show_date,
            })
        );
    },
    onRender: function(){
        this.showChildView(
            'payment_display',
            new SelectWidget(
                {
                    options: AppOption['form_options']['payment_display_options'],
                    title: "Affichage des paiements",
                    field_name: 'paymentDisplay',
                    id_key: 'value',
                    value: this.model.get('paymentDisplay'),
                }
            )
        );
        this.showChildView(
            'deposit',
            new SelectWidget(
                {
                    options: AppOption['form_options']['deposit_options'],
                    title: "Acompte à la commande",
                    field_name: 'deposit',
                    id_key: 'value',
                    value: this.model.get('deposit'),
                }
            )
        );
        this.showChildView(
            'payment_times',
            new SelectWidget(
                {
                    options: AppOption['form_options']['payment_times_options'],
                    title: "Paiement en",
                    field_name: 'payment_times',
                    id_key: 'value',
                    value: this.model.get('payment_times'),
                }
            )
        );
        this.renderTable();
    }
});
export default PaymentBlockView;
