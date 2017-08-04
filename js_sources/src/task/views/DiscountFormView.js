/*
 * File Name : DiscountFormView.js
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
import SelectWidget from './SelectWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import FormBehavior from '../behaviors/FormBehavior.js';
import { getOpt } from '../../tools.js';
import Radio from 'backbone.radio';
var template = require('./templates/DiscountFormView.mustache');

const DiscountFormView = Mn.View.extend({
    behaviors: [FormBehavior],
    template: template,
    regions: {
        'description': '.description',
        'amount': '.amount',
        'tva': '.tva',
    },
    childViewTriggers: {
        'change': 'data:modified',
    },
    initialize(){
        var channel = Radio.channel('facade');
        this.tva_options = channel.request('get:form_options', 'tvas');
    },
    onRender: function(){
        this.showChildView(
            'description',
            new TextAreaWidget({
                value: this.model.get('description'),
                title: "Description",
                field_name: "description",
                tinymce: true,
                cid: this.model.cid
            })
        );
        this.showChildView(
            'amount',
            new InputWidget(
                {
                    value: this.model.get('amount'),
                    title: "Montant",
                    field_name: "amount",
                    addon: '€',
                }
            )
        );
        this.showChildView(
            'tva',
            new SelectWidget(
                {
                    options: this.tva_options,
                    title: "TVA",
                    value: this.model.get('tva'),
                    id_key: 'value',
                    field_name: 'tva'
                }
            )
        );
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
        };
    }
});
export default DiscountFormView;
