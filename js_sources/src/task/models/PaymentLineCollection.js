/*
 * File Name : PaymentLineCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import OrderableCollection from "./OrderableCollection.js";
import PaymentLineModel from './PaymentLineModel.js';
import Radio from 'backbone.radio';
import { getPercent } from '../../math.js';

const PaymentLineCollection = OrderableCollection.extend({
    model: PaymentLineModel,
    url: function(){
        return AppOption['context_url'] + '/' + 'payment_lines';
    },
    initialize(options){
        PaymentLineCollection.__super__.initialize.apply(this, options);
        this.channel = Radio.channel('facade');
        this.totalmodel = this.channel.request('get:totalmodel');
        this.callChannel = this.callChannel.bind(this);
        this.bindEvents();
    },
    bindEvents(){
        console.log("PaymentLineCollection.bindEvents");
        this.listenTo(this, 'add', this.callChannel);
        this.listenTo(this, 'remove', this.callChannel);
        this.listenTo(this, 'change:amount', this.callChannel);
    },
    unBindEvents(){
        console.log("PaymentLineCollection.unBindEvents");
        this.stopListening();
    },
    callChannel(){
        this.channel.trigger('changed:payment_lines');
    },
    computeDividedAmount(total, payment_times){
        var result = 0;
        if (payment_times > 1){
            result = Math.round(total * 100 / payment_times);
        }
        return result / 100;
    },
    depositAmount(deposit){
        var total = this.totalmodel.get('ttc');
        deposit = parseInt(deposit, 10);
        var deposit_amount = 0;
        if (deposit > 0){
            deposit_amount = getPercent(total, deposit);
        }
        return deposit_amount;
    },
    topayAfterDeposit(deposit){
        var total = this.totalmodel.get('ttc');
        var deposit_amount = this.depositAmount(deposit);
        return total - deposit_amount;
    },
    genPaymentLines(payment_times, deposit){
        console.log("Gen payment lines");
        this.unBindEvents();
        var total = this.topayAfterDeposit(deposit);

        var description = 'Livrable';
        var part = 0;
        console.log("Total : %s", total);
        if(payment_times > 1){
            part = this.computeDividedAmount(total, payment_times);
        }
        console.log(" + Part %s", part);

        var models = this.slice(0, payment_times);
        var model;
        var i;
        for (i=1; i < payment_times; i++){
            if (models.length >= i){
                model = models[i -1];
            } else {
                model = new PaymentLineModel({order: i-1});
            }
            model.set({amount: part, description: description});
            description = "Paiement " + (i + 1);
            models[i-1] = model;
        }
        i = payment_times;
        // Rest is equal to total if payment_times <=1
        var rest = total - ( (payment_times-1) * part );
        if (models.length >= i){
            model = models[i -1];
        } else {
            model = new PaymentLineModel();
        }
        model.set({amount: rest, description: "Solde"});
        models[i -1] = model;
        var old_models = this.models.slice(payment_times);
        this.set(models);
        console.log("New number of models : %s", this.models.length);
        this.updateModelOrder(false);
        return this.syncAll(old_models);
    },
    syncAll(old_models){
        console.log("Syncing all models");
        var promises = [];
        var collection_url = this.url();
        _.each(old_models, function(model){
            // Here the model is not attached to the collection anymore, we
            // manually set the urlRoot
            model.urlRoot = collection_url;
            promises.push(model.destroy(
                {
                    'success': function(){
                        console.log("Suppression d'échéances : OK");
                    }
                }
            ));
        });
        this.each(function(model){
            promises.push(
                model.save(
                    null,
                    {'wait': true, 'sync':true, patch: true}
                )
            );
        });
        var resulting_deferred = $.when(...promises).then(this.afterSyncAll.bind(this));
        return resulting_deferred;
    },
    afterSyncAll(){
        console.log("The PaymentLineCollection was synced");
        this.bindEvents();
    },
    getSoldAmount(deposit){
        let ttc = this.topayAfterDeposit(deposit);
        let sum = 0;
        let models = this.slice(0, this.models.length - 1);
        _.each(models, function(item){
            sum += item.getAmount();
        });
        return ttc - sum;
    },
    updateSold(deposit){
        console.log("Updating sold");
        this.unBindEvents();
        var value = this.getSoldAmount(deposit);
        this.models[this.models.length - 1].set({'amount': value});
        this.models[this.models.length - 1].save().then(this.afterSyncAll.bind(this));
    },
    validate: function(){
        var result = {};
        this.each(function(model){
            var res = model.validate();
            if (res){
                _.extend(result, res);
            }
        });
        return result;
    }
});
export default PaymentLineCollection;
