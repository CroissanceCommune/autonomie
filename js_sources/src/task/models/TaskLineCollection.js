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
import Bb from 'backbone';
import TaskLineModel from './TaskLineModel.js';
import Radio from 'backbone.radio';
import {ajax_call} from '../../tools.js';

const TaskLineCollection = Bb.Collection.extend({
    model: TaskLineModel,
    comparator: 'order',
    initialize: function(options) {
        this.on('change:reorder', this.updateModelOrder);
        this.updateModelOrder(false);
        this.on('remove', this.channelCall);
        this.on('sync', this.channelCall);
        this.on('reset', this.channelCall);
    },
    channelCall: function(){
        var channel = Radio.channel('facade');
        channel.trigger('changed:task');
    },
    updateModelOrder: function(sync){
        var sync = sync || true;
        this.each(function(model, index) {
            model.set('order', index);
            if (sync){
                model.save(
                    {'order': index},
                    {patch: true},
                );
            }
        });

    },
    getMinOrder: function(){
        if (this.models.length == 0){
            return 0
        }
        let first_model = _.min(
            this.models,
            function(model){return model.get('order')}
        );
        return first_model.get('order');
    },
    getMaxOrder: function(){
        if (this.models.length == 0){
            return 0
        }
        let last_model = _.max(
            this.models,
            function(model){return model.get('order')}
        );
        return last_model.get('order');
    },
    moveUp: function(model) { // I see move up as the -1
        var index = this.indexOf(model);
        if (index > 0) {
            this.models.splice(index - 1, 0, this.models.splice(index, 1)[0]);
            this.trigger('change:reorder');
        }
    },
    moveDown: function(model) {
        // I see move up as the -1
        var index = this.indexOf(model);
        if (index < this.models.length) {
            this.models.splice(index + 1, 0, this.models.splice(index, 1)[0]);
            this.trigger('change:reorder');
        }
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
    }
});
export default TaskLineCollection;
