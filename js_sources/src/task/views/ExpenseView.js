/*
 * File Name : ExpenseView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import FormBehavior from '../behaviors/FormBehavior.js';
import InputWidget from './InputWidget.js';

const ExpenseView = Mn.View.extend({
    template: require('./templates/ExpenseView.mustache'),
    regions: {
        expense_container: '.expense-container'
    },
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    behaviors: [
        {
            behaviorClass: FormBehavior,
            errorMessage: "Vérifiez votre saisie"
        }
    ],
    onRender: function(){
        this.showChildView(
            'expense_container',
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
export default ExpenseView;
