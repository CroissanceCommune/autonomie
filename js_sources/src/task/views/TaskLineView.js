/*
 * File Name : TaskLineView.js
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

const template = require('./templates/TaskLineView.mustache');

const TaskLineView = Mn.View.extend({
    tagName: 'div',
    className: 'row taskline',
    template: template,
    ui:{
        up_button: 'button.up',
        down_button: 'button.down',
        edit_button: 'button.edit',
        delete_button: 'button.delete'
    },
    triggers: {
        'click @ui.up_button': 'order:up',
        'click @ui.down_button': 'order:down',
        'click @ui.edit_button': 'edit',
        'click @ui.delete_button': 'delete'
    },
    modelEvents: {
        'change': 'render'
    },
    initialize(){
        var channel = Radio.channel('config');
        this.tva_options = channel.request('get:options', 'tvas');
        this.product_options = channel.request('get:options', 'products');
    },
    getTvaLabel(){
        let res = "";
        let current_value = this.model.get('tva');
        _.each(this.tva_options, function(tva){
            if (tva.value == current_value){
                res = tva.name;
            }
        });
        return res
    },
    getProductLabel(){
        let res = "";
        let current_value = this.model.get('product_id');
        _.each(this.product_options, function(product){
            if (product.id == current_value){
                res = product.label;
            }
        });
        return res
    },
    templateContext(){
        let min_order = this.model.collection.getMinOrder();
        let max_order = this.model.collection.getMaxOrder();
        let order = this.model.get('order');
        return {
            ht: formatAmount(this.model.ht(), false),
            product: this.getProductLabel(),
            tva_label: this.getTvaLabel(),
            is_not_first: order != min_order,
            is_not_last: order != max_order
        };

    }
});
export default TaskLineView;
