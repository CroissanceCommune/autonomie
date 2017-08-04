/*
 * File Name : DiscountView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import Mn from 'backbone.marionette';
import { formatAmount } from '../../math.js';
import Radio from 'backbone.radio';

const template = require('./templates/DiscountView.mustache');

const DiscountView = Mn.View.extend({
    template: template,
    ui:{
        edit_button: 'button.edit',
        delete_button: 'button.delete'
    },
    // Trigger to the parent
    triggers: {
        'click @ui.edit_button': 'edit',
        'click @ui.delete_button': 'delete'
    },
    modelEvents: {
        'change': 'render'
    },
    initialize(){
        var channel = Radio.channel('facade');
        this.tva_options = channel.request('get:options', 'tvas');
    },
    getTvaLabel(){
        let res = "";
        let current_value = this.model.get('tva');
        _.each(
            this.tva_options,
            function(tva){
                if (tva.value == current_value){
                    res = tva.name;
                }
            }
        );
        return res
    },
    templateContext(){
        return {
            ht: formatAmount(this.model.ht()),
            tva_label: this.getTvaLabel(),
        };
    }
});
export default DiscountView;
