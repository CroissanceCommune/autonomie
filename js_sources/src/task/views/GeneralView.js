/*
 * File Name : GeneralView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import jQuery from 'jquery';
import Mn from 'backbone.marionette';
import { updateSelectOptions } from '../../tools.js';
import FormBehavior from "../behaviors/FormBehavior.js";
import CheckboxListWidget from './CheckboxListWidget.js';
import DatePickerWidget from './DatePickerWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import InputWidget from './InputWidget.js';

var template = require("./templates/GeneralView.mustache");


const GeneralView = Mn.View.extend({
    /*
     * Wrapper around the component making part of the 'common'
     * invoice/estimation form, provide a main layout with regions for each
     * field
     */
    behaviors: [
        {
            behaviorClass: FormBehavior,
            errorMessage: "Vérifiez votre saisie"
        }
    ],
    tagName: 'div',
    className: 'form-section',
    template: template,
    regions: {
        name: '.name',
        prefix: '.prefix',
        financial_year: '.financial_year',
    },
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    initialize(options){
        this.section = options['section'];
    },
    templateContext: function(){
        return {};
    },
    onRender: function(){
        this.showChildView(
            'name',
            new InputWidget({
                title: "Nom du document",
                value: this.model.get('name'),
                field_name: 'name',
            })
        );
        if (_.has(this.section, 'prefix')){
            this.showChildView(
                'prefix',
                new InputWidget({
                    title: "Préfixe du numéro de facture",
                    value: this.model.get('prefix'),
                    field_name: 'prefix',
                })
            );
        }
        if (_.has(this.section, 'financial_year')){
            this.showChildView(
                'financial_year',
                new InputWidget({
                    title: "Année comptable de référence",
                    value: this.model.get('financial_year'),
                    field_name: 'financial_year',
                })
            );
        }
    }
});
export default GeneralView;
