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
import ModalFormBehavior from '../behaviors/ModalFormBehavior.js';
import { getOpt } from '../../tools.js';
var template = require('./templates/DiscountFormView.mustache');

const DiscountFormView = Mn.View.extend({
    template: template,
    regions: {
        'description': '.description',
        'amount': '.amount',
        'tva': '.tva',
        'percentage': '.percentage',
    },
    ui: {
        btn_cancel: "button[type=reset]",
        form: "form",
        submit: 'button[type=submit]',
        main_tab: 'ul.nav-tabs li:first a'
    },
    behaviors: [ModalFormBehavior],
    triggers: {
        'click @ui.btn_cancel': 'modal:close'
    },
    childViewEvents: {
        'change': 'onChildChange',
        'catalog:edit': 'onCatalogEdit'
    },
    modelEvents: {
        'change': 'refreshForm'
    },
    refreshForm: function(){

    },
    isAddView: function(){
        return !getOpt(this, 'edit', false);
    },
    refreshForm: function(){
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
                    options: AppOption['form_options']['tva_options'],
                    title: "TVA",
                    value: this.model.get('tva'),
                    field_name: 'tva'
                }
            )
        );
        if (this.isAddView()){
            this.getUI('main_tab').tab('show');
        }
    },
    onRender: function(){
        this.refreshForm();
        if (this.isAddView()){
            this.showChildView(
                'percentage',
                new InputWidget(
                    {
                        title: "Pourcentage",
                        field_name: 'percentage',
                        addon: "%"
                    }
                )
            );
        }
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            add: this.isAddView(),
        }
    }
});
export default DiscountFormView;
