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
import StatusHistoryCollection from '../models/StatusHistoryCollection.js';
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
        'save:model': 'saveModel',
    },
    radioRequests: {
        'get:model': 'getModelRequest',
        'get:collection': 'getCollectionRequest',
        'get:paymentcollection': 'getPaymentCollectionRequest',
        'get:totalmodel': 'getTotalModelRequest',
        'get:form_options': 'getFormOptions',
        'has:form_section': 'hasFormSection',
        'get:form_actions': 'getFormActions',
        'is:estimation_form': 'isEstimationForm',
        'get:status_history_collection': 'getStatusHistory',
        'is:valid': "isDataValid",
    },
    initialize(options){
        this.syncModel = this.syncModel.bind(this);
    },
    setFormConfig(form_config){
        this.form_config = form_config;
    },
    loadModels(form_datas){
        this.models = {};
        this.collections = {};
        if (_.isUndefined(this.form_config)){
            throw "setFormConfig shoud be fired before loadModels";
        }
        this.totalmodel = new TotalModel();
        this.models['common'] = new CommonModel(form_datas);
        this.models['common'].url = AppOption['context_url'];

        var lines = form_datas['line_groups'];
        this.collections['task_groups'] = new TaskGroupCollection(lines);

        var discounts = form_datas['discounts'];
        this.collections['discounts'] = new DiscountCollection(discounts);
        this.computeTotals();

        if (_.has(form_datas, 'payment_lines')){
            var payment_lines = form_datas['payment_lines'];
            this.payment_lines_collection = new PaymentLineCollection(
                payment_lines
            );
        }

        if (_.has(form_datas, 'status_history')){
            var history = form_datas['status_history'];
            this.status_history_collection = new StatusHistoryCollection(
                history
            );
        }
    },
    getFormOptions(option_name){
        /*
         * Return the form options for option_name
         *
         * :param str option_name: The name of the option
         * :returns: A list of dict with options (for building selects)
         */
        console.log("FacadeClass.getFormOptions");
        return this.form_config['options'][option_name];
    },
    hasFormSection(section_name){
        /*
         * Check if the given section should be part of the current form
         *
         * :param str section_name: The name of the section
         */
        return _.indexOf(this.form_config['sections'], section_name) >= 0;
    },
    getFormActions(){
        /*
         * Return available form action config
         */
        return this.form_config['actions'];
    },
    getStatusHistory(){
        return this.status_history_collection;
    },
    isEstimationForm(){
        return this.form_config['is_estimation'];
    },
    syncModel(modelName){
        var modelName = modelName || 'common';
        this.models[modelName].save(null, {wait:true, sync: true, patch:true});
    },
    saveModel(view, model, datas, extra_options, success, error){
        /*
         * Save a model
         *
         * :param obj model: The model to save
         * :param obj datas: The datas to transmit to the save call
         * :param obj extra_options: The options to pass to the save call
         * :param func success: The success callback
         * :param func error: The error callback
         */
        var options = {
            wait: true,
            patch: true
        };
        _.extend(options, extra_options);
        options['success'] = success;
        options['error'] = error;

        model.save(datas, options);
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
    },
    isDataValid(){
        var channel = Radio.channel('facade');
        channel.trigger('bind:validation');
        var result = {};
        _.each(this.models, function(model){
            var res = model.validate();
            if (res){
                _.extend(result, res);
            }
        });
        _.each(
            this.collections,
            function(collection){
                var res = collection.validate();
                if (res){
                    _.extend(result, res);
                }
            }
        );
        channel.trigger('unbind:validation');
        return result;
    }
});
const Facade = new FacadeClass();
export default Facade;
