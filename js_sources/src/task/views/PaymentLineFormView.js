/*
 * File Name : PaymentLineFormView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import InputWidget from './InputWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import ModalFormBehavior from '../behaviors/ModalFormBehavior.js';
import { ajax_call, getOpt } from '../../tools.js';
import DatePickerWidget from './DatePickerWidget.js';

var template = require('./templates/PaymentLineFormView.mustache');

const PaymentLineFormView = Mn.View.extend({
    behaviors: [ModalFormBehavior],
    template: template,
    regions: {
        'order': '.order',
        'description': ".description",
        "date": ".date",
        "amount": ".amount",
    },
    onRender: function(){
        this.showChildView(
            'order',
            new InputWidget({
                value: this.model.get('order'),
                field_name:'order',
                type: 'hidden',
            })
        );
        var view = new TextAreaWidget(
            {
                field_name: "description",
                value: this.model.get('description'),
                title: "Intitulé",
            }
        );
        this.showChildView('description', view);

        if (this.getOption('show_date')){
            view = new DatePickerWidget(
                {
                    date: this.model.get('date'),
                    title: "Date",
                    field_name: "date"
                }
            );
        }
        this.showChildView('date', view);

        if (this.getOption('edit_amount')){
            view = new InputWidget(
                {
                    field_name: 'amount',
                    value: this.model.get('amount'),
                    title: "Montant",
                }
            );
            this.showChildView('amount', view);
        }
    },
    templateContext(){
        return {
            title: this.getOption('title')
        }
    }
});
export default PaymentLineFormView;
