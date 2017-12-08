/*
 * File Name : ExpenseHtBlockView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import FormBehavior from '../../base/behaviors/FormBehavior.js';
import InputWidget from '../../widgets/InputWidget.js';

var template = require('./templates/ExpenseHtBlockView.mustache');

const ExpenseHtBlockView = Mn.View.extend({
    template: template,
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
        expenses_ht: ".expenses_ht",
    },
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    initialize(options){
        this.section = options['section'];
    },
    onRender: function(){
        this.showChildView(
            'expenses_ht',
            new InputWidget(
                {
                    title: "Frais forfaitaires (HT)",
                    value: this.model.get('expenses_ht'),
                    field_name:'expenses_ht',
                }
            )
        );
    }
});
export default ExpenseHtBlockView;
