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

const DiscountCollection = Bb.Collection.extend({
    model: DiscountModel,
    url: function(){
        return AppOption['context_url'] + '/' + 'discount_lines';
    },
    ht: function(){
        var result = 0;
        this.each(function(model){
            result += model.ht();
        });
        return -1 * result;
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
export default DiscountCollection;
