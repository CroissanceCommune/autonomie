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
import SelectWidget from '../../widgets/SelectWidget.js';
import TextAreaWidget from '../../widgets/TextAreaWidget.js';
import {findCurrentSelected} from '../../tools.js';
import FormBehavior from '../../base/behaviors/FormBehavior.js';
import PaymentLineTableView from './PaymentLineTableView.js';
import Radio from 'backbone.radio';
import Validation from 'backbone-validation';

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
        'change:payment_times': 'onPaymentTimesChange',
        'change:paymentDisplay': 'onPaymentDisplayChange',
    },
    childViewEvents: {
        'finish': 'onFinish',
    },
    initialize: function(options){
        this.collection = options['collection'];
        var channel = Radio.channel('config');
        this.payment_display_options = channel.request(
            'get:options',
            'payment_displays'
        );
        this.deposit_options = channel.request(
            'get:options',
            'deposits',
        );
        this.payment_times_options = channel.request(
            'get:options',
            'payment_times'
        );
        channel = Radio.channel('facade');
        this.listenTo(channel, 'bind:validation', this.bindValidation);
        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
    },
    bindValidation(){
        Validation.bind(this);
    },
    unbindValidation(){
        Validation.unbind(this);
    },
    onPaymentTimesChange(model, value){
        var old_value = model.previous('payment_times');
        console.log("Old value was %s", old_value);
        if ((value == -1) || (old_value == -1)){
            this.renderTable();
        }
    },
    onPaymentDisplayChange(model, value){
        var old_value = model.previous('paymentDisplay');
        console.log("Old value was %s", old_value);
        // If it changed and it is or was ALL_NO_DATE we render the lines again
        if ((old_value != value) && _.indexOf([value, old_value], 'ALL_NO_DATE') != -1){
            this.renderTable();
        }
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
        } else if (field_name == 'payment_times'){
            var old_value = this.model.get('payment_times');
            if (old_value != value){
                if (value != -1){
                    // We generate the payment lines (and delete old ones)
                    var this_ = this;
                    var deferred = this.collection.genPaymentLines(
                        value,
                        this.model.get('deposit')
                    );

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
            }
        } else if (field_name == 'deposit'){
            var old_value = this.model.get('deposit');

            if (old_value != value){
                this.triggerMethod('data:persist', field_name, value);
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
        this.tableview = new PaymentLineTableView({
            collection: this.collection,
            model: this.model,
            edit: edit,
            show_date: show_date,
        });
        this.showChildView('lines', this.tableview);
    },
    onRender: function(){
        this.showChildView(
            'payment_display',
            new SelectWidget(
                {
                    options: this.payment_display_options,
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
                    options: this.deposit_options,
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
                    options: this.payment_times_options,
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
