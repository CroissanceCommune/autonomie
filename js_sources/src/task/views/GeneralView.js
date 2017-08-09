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
import FormBehavior from "../../base/behaviors/FormBehavior.js";
import CheckboxListWidget from '../../widgets/CheckboxListWidget.js';
import DatePickerWidget from '../../widgets/DatePickerWidget.js';
import TextAreaWidget from '../../widgets/TextAreaWidget.js';
import InputWidget from '../../widgets/InputWidget.js';
import StatusHistoryView from './StatusHistoryView.js';
import Radio from 'backbone.radio';

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
        status_history: '.status_history',
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
        this.attachments = Radio.channel('facade').request('get:attachments');
    },
    templateContext: function(){
        return {attachments: this.attachments};
    },
    showStatusHistory(){
        var collection = Radio.channel('facade').request(
            'get:status_history_collection'
        );
        if (collection.models.length > 0){
            var view = new StatusHistoryView({collection: collection});
            this.showChildView('status_history', view);
        }
    },
    onRender: function(){
        this.showStatusHistory();
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
