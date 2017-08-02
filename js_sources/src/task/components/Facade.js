/*
 * File Name : Facade.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';

import CommonModel from "../models/CommonModel.js";
import TaskGroupCollection from '../models/TaskGroupCollection.js';
import DiscountCollection from '../models/DiscountCollection.js';
import PaymentLineCollection from '../models/PaymentLineCollection.js';
import TotalModel from '../models/TotalModel.js';
import Radio from 'backbone.radio';

const FacadeClass = Mn.Object.extend({
    channelName: 'facade',
    ht: 5,
    radioEvents: {
        'changed:task': 'computeTotals',
        'changed:discount': 'computeMainTotals',
        'changed:expense_ht': 'computeMainTotals',
        'changed:payment_lines': "updatePaymentLines",
        'sync:model': 'syncModel',
    },
    radioRequests: {
        'get:model': 'getModelRequest',
        'get:collection': 'getCollectionRequest',
        'get:paymentcollection': 'getPaymentCollectionRequest',
        'get:totalmodel': 'getTotalModelRequest',
    },
    initialize(options){
        this.models = {};
        this.collections = {};
        this.totalmodel = new TotalModel();
        this.syncModel = this.syncModel.bind(this);
    },
    loadModels(datas){
        this.models['common'] = new CommonModel(datas);
        this.models['common'].url = AppOption['context_url'];

        var lines = datas['line_groups'];
        this.collections['task_groups'] = new TaskGroupCollection(lines);

        var discounts = datas['discounts'];
        this.collections['discounts'] = new DiscountCollection(discounts);
        this.computeTotals();

        if (_.has(datas, 'payment_lines')){
            var payment_lines = datas['payment_lines'];
            this.payment_lines_collection = new PaymentLineCollection(
                payment_lines
            );
        }
    },
    syncModel(modelName){
        var modelName = modelName || 'common';
        console.log(modelName);
        console.log(this.models);
        this.models[modelName].save(null, {wait:true, sync: true, patch:true});
    },
    getPaymentCollectionRequest(){
        return this.payment_lines_collection;
    },
    getTotalModelRequest(){
        return this.totalmodel;
    },
    getModelRequest(label){
        return this.models[label];
    },
    getCollectionRequest(label){
        return this.collections[label];
    },
    updatePaymentLines(){
        var channel = Radio.channel('facade');
        channel.trigger('update:payment_lines', this.totalmodel);
    },
    computeTotals(){
        this.totalmodel.set({
            'ht_before_discounts': this.tasklines_ht(),
            'ht': this.HT(),
            'tvas': this.TVAParts(),
            'ttc': this.TTC()
        });
    },
    computeMainTotals(){
        this.totalmodel.set({
            'ht_before_discounts': this.tasklines_ht(),
            'ht': this.HT(),
            'tvas': this.TVAParts(),
            'ttc': this.TTC()
        });
    },
    tasklines_ht(){
        return this.collections['task_groups'].ht();
    },
    HT(){
        var result = 0;
        _.each(this.collections, function(collection){
            result += collection.ht();
        });
        _.each(this.models, function(model){
            result += model.ht();
        });
        return result;
    },
    TVAParts(){
        var result = {};
        _.each(this.collections, function(collection){
            var tva_parts = collection.tvaParts();
            _.each(tva_parts, function(value, key){
                if (key in result){
                    value += result[key];
                }
                result[key] = value;
            });
        });
        _.each(this.models, function(model){
            var tva_parts = model.tvaParts();
            _.each(tva_parts, function(value, key){
                if (key in result){
                    value += result[key];
                }
                result[key] = value;
            });
        });
        return result;
    },
    TTC(){
        var result = 0;
        _.each(this.collections, function(collection){
            result += collection.ttc();
        });
        _.each(this.models, function(model){
            result += model.ttc();
        });
        return result;
    }
});
const Facade = new FacadeClass();
export default Facade;
