/*
 * File Name : TaskGroupCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import OrderableCollection from "./OrderableCollection.js";
import TaskGroupModel from './TaskGroupModel.js';
import { ajax_call } from '../../tools.js';
import Radio from 'backbone.radio';


const TaskGroupCollection = OrderableCollection.extend({
    model: TaskGroupModel,
    url: function(){
        return AppOption['context_url'] + '/' + 'task_line_groups';
    },
    initialize: function(options) {
        TaskGroupCollection.__super__.initialize.apply(this, options);
        this.on('remove', this.channelCall);
        this.on('sync', this.channelCall);
        this.on('reset', this.channelCall);
    },
    channelCall: function(){
        var channel = Radio.channel('facade');
        channel.trigger('changed:task');
    },
    load_from_catalog: function(sale_product_group_ids){
        var serverRequest = ajax_call(
            this.url() + '?action=load_from_catalog',
            {sale_product_group_ids: sale_product_group_ids},
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
    ttc: function(){
        var result = 0;
        this.each(function(model){
            result += model.ttc();
        });
        return result;
    }
});
export default TaskGroupCollection;
