/*
 * File Name : TaskLineCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import TaskLineModel from './TaskLineModel.js';
import Radio from 'backbone.radio';
import {ajax_call} from '../../tools.js';
import OrderableCollection from "./OrderableCollection.js";

const TaskLineCollection = OrderableCollection.extend({
    model: TaskLineModel,
    initialize: function(options) {
        TaskLineCollection.__super__.initialize.apply(this, options);
        this.on('remove', this.channelCall);
        this.on('sync', this.channelCall);
        this.on('reset', this.channelCall);
    },
    channelCall: function(){
        var channel = Radio.channel('facade');
        channel.trigger('changed:task');
    },
    load_from_catalog: function(sale_product_ids){
        var serverRequest = ajax_call(
            this.url + '?action=load_from_catalog',
            {sale_product_ids: sale_product_ids},
            'POST'
        );
        serverRequest.then(this.fetch.bind(this));
    },
    ht: function(){
        var result = 0;
        this.each(function(model){
            result += model.ht();
        });
        return result;
    },
    tvaParts: function(){
        var result = {};
        this.each(function(model){
            var tva_amount = model.tva();
            var tva = model.get('tva');
            if (tva in result){
                tva_amount += result[tva];
            }
            result[tva] = tva_amount;
        });
        return result;
    },
    ttc: function(){
        var result = 0;
        this.each(function(model){
            result += model.ttc();
        });
        return result;
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
export default TaskLineCollection;
