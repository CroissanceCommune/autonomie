/*
 * File Name : CommonView.js
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
import CheckboxListView from './CheckboxListView.js';
import DatePickerView from './DatePickerView.js';
import TextAreaView from './TextAreaView.js';

var template = require("./templates/CommonView.mustache");


const CommonView = Mn.View.extend({
    /*
     * Wrapper around the component making part of the 'common'
     * invoice/estimation form, provide a main layout with regions for each
     * field
     */
    template: template,
    formname: "common",
    regions: {
        mentions: '.mentions',
        date: '.date',
        description: '.description',
        address: '.address',
        workplace: '.workplace',
    },
    behaviors: [
        {
            behaviorClass: FormBehavior,
            errorMessage: "Vérifiez votre saisie"
        }
    ],
    childViewEvents: {
        'change': 'onChildChange',
        'finish': 'onChildFinish'
    },
    onChildChange: function(attribute, value){
        this.triggerMethod('data:modified', this, attribute, value);
    },
    onChildFinish: function(attribute, value){
        this.triggerMethod('data:persist', this, attribute, value);
    },
    getMentionOptions: function(){
        var mention_options = AppOption['form_options']['mention_options'];
        var mentions = this.model.get('mentions');
        var mention_ids = [];
        _.each(mentions, function(mention){
            mention_ids.push(mention.id);
        });
        updateSelectOptions(mention_options, mention_ids, 'id');
        return mention_options;
    },
    onRender: function(){
        const mention_list = new CheckboxListView({
            options: this.getMentionOptions(),
            title: "Mentions facultatives",
            description: "Choisissez les mentions à ajouter au document",
            field_name: "mentions"
        });
        this.showChildView('mentions', mention_list);

        this.showChildView('date', new DatePickerView({
            date: this.model.get('date'),
            title: "Date",
            field_name: "date"
        }));

        this.showChildView('address', new TextAreaView({
            title: 'Adresse du client',
            value: this.model.get('address'),
            field_name: 'address',
            rows: 5
        }));

        this.showChildView('description', new TextAreaView({
            title: 'Objet du document',
            value: this.model.get('description'),
            field_name: 'description',
            rows: 3
        }));

        this.showChildView('workplace', new TextAreaView({
            title: 'Lieu des travaux',
            value: this.model.get('workplace'),
            field_name: 'workplace',
            rows: 3
        }));
    }
});
export default CommonView;
