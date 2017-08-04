/*
 * File Name : DiscountCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import DiscountModel from './DiscountModel.js';
import Radio from 'backbone.radio';
import { ajax_call } from '../../tools.js';


const DiscountCollection = Bb.Collection.extend({
    model: DiscountModel,
    initialize: function(options) {
        this.on('remove', this.channelCall);
        this.on('sync', this.channelCall);
        this.on('reset', this.channelCall);
    },
    channelCall: function(){
        var channel = Radio.channel('facade');
        channel.trigger('changed:discount');
    },
    url: function(){
        return AppOption['context_url'] + '/' + 'discount_lines';
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
    insert_percent: function(model){
        /*
         * Call the server to generate percent based Discounts
         * :param obj model: A DiscountPercentModel instance
         */
        var serverRequest = ajax_call(
            this.url() + '?action=insert_percent',
            model.toJSON(),
            'POST'
        );
        serverRequest.then(this.fetch.bind(this));
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
export default DiscountCollection;
