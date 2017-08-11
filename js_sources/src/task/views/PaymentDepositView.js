/*
 * File Name : PaymentDepositView.js
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

const PaymentDepositView = Mn.View.extend({
    className: 'row taskline',
    template: require('./templates/PaymentDepositView.mustache'),
    modelEvents: {
        'change:amount': 'render'
    },
    templateContext(){
        return {
            show_date: this.getOption('show_date'),
            amount_label: formatAmount(this.model.get('amount'))
        }
    }
});
export default PaymentDepositView;
