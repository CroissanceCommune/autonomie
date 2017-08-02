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
    regions: {
        mentions: '.mentions',
        date: '.date',
        description: '.description',
        address: '.address',
        workplace: '.workplace',
    },
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    getMentionIds: function(){
        var mentions = this.model.get('mentions');
        var mention_ids = [];
        _.each(mentions, function(mention){
            mention_ids.push(mention.id);
        });
        return mention_ids;
    },
    isMoreSet: function(){
        var mention_ids = this.getMentionIds();
        if (mention_ids.length > 0){
            return true;
        }
        if (this.model.get('workplace')){
            return true;
        }
        return false;
    },
    templateContext: function(){
        return {is_more_set: this.isMoreSet()};
    },
    onRender: function(){
        const mention_list = new CheckboxListWidget({
            options: AppOption['form_options']['mention_options'],
            value: this.getMentionIds(),
            title: "Mentions facultatives",
            description: "Choisissez les mentions à ajouter au document",
            field_name: "mentions"
        });
        this.showChildView('mentions', mention_list);

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
    }
});
export default CommonView;
