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
import CheckboxListWidget from './CheckboxListWidget.js';
import DatePickerWidget from './DatePickerWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import InputWidget from './InputWidget.js';
import Radio from 'backbone.radio';
import Validation from 'backbone-validation';

var template = require("./templates/CommonView.mustache");


const CommonView = Mn.View.extend({
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
    fields: [
        'date',
        'address',
        'description',
        'workplace',
        'mentions'
    ],
    regions: {
        errors: '.errors',
        date: '.date',
        description: '.description',
        address: '.address',
        workplace: '.workplace',
        mentions: '.mentions',
    },
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    modelEvents: {
        'validated:invalid': 'showErrors',
        'validated:valid': 'hideErrors',
    },
    initialize(){
        var channel = Radio.channel('facade');
        this.listenTo(channel, 'bind:validation', this.bindValidation);
        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
        this.mentions_options = channel.request('get:form_options', 'mentions');
    },
    showErrors(model, errors){
        this.$el.addClass('error');
    },
    hideErrors(model){
        this.$el.removeClass('error');
    },
    bindValidation(){
        Validation.bind(this, {attributes: this.fields});
    },
    unbindValidation(){
        Validation.unbind(this);
    },
    getMentionIds(){
        var mentions = this.model.get('mentions');
        var mention_ids = [];
        _.each(mentions, function(mention){
            mention_ids.push(mention.id);
        });
        return mention_ids;
    },
    isMoreSet(){
        var mention_ids = this.getMentionIds();
        if (mention_ids.length > 0){
            return true;
        }
        if (this.model.get('workplace')){
            return true;
        }
        return false;
    },
    templateContext(){
        return {is_more_set: this.isMoreSet()};
    },
    onRender(){
        this.showChildView('date', new DatePickerWidget({
            date: this.model.get('date'),
            title: "Date",
            field_name: "date"
        }));

        this.showChildView('address', new TextAreaWidget({
            title: 'Adresse du client',
            value: this.model.get('address'),
            field_name: 'address',
            rows: 5
        }));

        this.showChildView('description', new TextAreaWidget({
            title: 'Objet du document',
            value: this.model.get('description'),
            field_name: 'description',
            rows: 3
        }));

        this.showChildView('workplace', new TextAreaWidget({
            title: 'Lieu des travaux',
            value: this.model.get('workplace'),
            field_name: 'workplace',
            rows: 3
        }));
        const mention_list = new CheckboxListWidget({
            options: this.mentions_options,
            value: this.getMentionIds(),
            title: "Mentions facultatives",
            description: "Choisissez les mentions à ajouter au document",
            field_name: "mentions"
        });
        this.showChildView('mentions', mention_list);
    }
});
export default CommonView;
