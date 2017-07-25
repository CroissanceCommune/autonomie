/*
 * File Name : TaskLineFormView.js
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

var template = require('./templates/TaskLineFormView.mustache');

const TaskLineFormView = Mn.View.extend({
    template: template,
    regions: {
        'description': '.description',
        'cost': '.cost',
        'quantity': '.quantity',
        'unity': '.unity',
        'tva': '.tva',
        'product_id': '.product_id',
    },
    ui: {
        btn_cancel: "button[type=reset]",
        form: "form",
        submit: 'button[type=submit]',
    },
    behaviors: [ModalFormBehavior],
    triggers: {
        'click @ui.btn_cancel': 'close:modal'
    },
    childViewEvents: {
        'change': 'onChildChange'
    },
    onChildChange: function(attribute, value){
        this.triggerMethod('data:modified', this, attribute, value);
    },
    templateContext: function(){
        return {
            title: this.getOption('title')
        };
    },
    onRender: function(){
        this.showChildView(
            'description',
            new TextAreaWidget({
                value: this.model.get('description'),
                title: "Intitulé des postes",
                field_name: "description",
                tinymce: true,
                css_class: 'required',
                cid: this.model.cid
            })
        );
        this.showChildView(
            'cost',
            new InputWidget(
                {
                    value: this.model.get('cost'),
                    title: "Prix unitaire HT *",
                    css_class: 'required',
                    field_name: "cost"
                }
            )
        );
        this.showChildView(
            'quantity',
            new InputWidget(
                {
                    value: this.model.get('quantity'),
                    css_class: 'required',
                    title: "Quantité *",
                    field_name: "quantity"
                }
            )
        );
        this.showChildView(
            'unity',
            new SelectWidget(
                {
                    options: AppOption['form_options']['workunit_options'],
                    title: "Unité (optionelle)",
                    value: this.model.get('unity'),
                    field_name: 'unity'
                }
            )
        );
        this.showChildView(
            'tva',
            new SelectWidget(
                {
                    options: AppOption['form_options']['tva_options'],
                    title: "TVA",
                    css_class: 'required',
                    value: this.model.get('tva'),
                    field_name: 'tva'
                }
            )
        );
        this.showChildView(
            'product_id',
            new SelectWidget(
                {
                    options: AppOption['form_options']['product_options'],
                    title: "Code produit",
                    value: this.model.get('product_id'),
                    field_name: 'product_id',
                    id_key: 'id'
                }
            )
        );
    }
});
export default TaskLineFormView;
