/*
 * File Name : PaymentLineView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { formatAmount } from '../../math.js';

const PaymentLineView = Mn.View.extend({
    className: 'row',
    template: require('./templates/PaymentLineView.mustache'),
    modelEvents: {
        'change': 'render',
    },
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
    templateContext: function(){
        let min_order = this.model.collection.getMinOrder();
        let max_order = this.model.collection.getMaxOrder();
        let order = this.model.get('order');
        return {
            edit: this.getOption('edit'),
            show_date: this.getOption('show_date'),
            date: formatDate(this.model.get('date')),
            amount: formatAmount(this.model.get('amount')),
            is_not_first: order != min_order,
            is_not_before_last: order != max_order - 1,
            is_not_last: order != max_order
        }
    }
});
export default PaymentLineView;
