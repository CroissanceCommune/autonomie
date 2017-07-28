/*
 * File Name : DiscountPercentView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TextAreaWidget from './TextAreaWidget.js';
import InputWidget from './InputWidget.js';
import DiscountModel from '../models/DiscountModel.js';
import BaseFormBehavior from "../behaviors/BaseFormBehavior.js";

const DiscountPercentView = Mn.View.extend({
    behaviors: [BaseFormBehavior],
    template: require('./templates/DiscountPercentView.mustache'),
    regions: {
        'description': '.description',
        'percentage': '.percentage'
    },
    ui: {
        form: 'form',
        submit: "button[type=submit]",
        btn_cancel: "button[type=reset]",
    },
    triggers: {
        'click @ui.btn_cancel': 'cancel:form',
    },
    childViewTriggers: {
        'change': 'data:modified',
    },
    events: {
        'submit @ui.form': "onSubmit"
    },
    onSubmit: function(event){
        event.preventDefault();
        this.triggerMethod('insert:percent', this.model);
    },
    onRender: function(){
        this.showChildView(
            'description',
            new TextAreaWidget({
                title: "Description",
                field_name: "description",
                tinymce: true,
                cid: '11111'
            })
        );
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
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
        };
    }

});
export default DiscountPercentView;
