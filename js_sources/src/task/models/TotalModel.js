/*
 * File Name : TotalModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import { formatAmount } from '../../math.js';
import Radio from 'backbone.radio';

const TotalModel = Bb.Model.extend({
    initialize: function(){
        TotalModel.__super__.initialize.apply(this, arguments);
        var channel = this.channel = Radio.channel('facade');
        this.tva_options = channel.request('get:form_options', 'tvas');
    },
    getTvaLabel: function(tva_value, tva_key){
        let res = {
            'value': formatAmount(tva_value, true),
            'label': 'Tva Inconnue'
        };
        _.each(
            this.tva_options,
            function(tva){
                if (tva.value == tva_key){
                    res['label'] = tva.name;
                }
            }
        );
        return res
    },
    tva_labels: function(){
        var values = [];
        var this_ = this;
        _.each(this.get('tvas'), function(item, key){
            values.push(this_.getTvaLabel(item, key));
        });
        return values;
    }
});
export default TotalModel;
