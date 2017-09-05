/*
 * File Name : ExpenseFormView.js
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
import DatePickerWidget from '../../widgets/DatePickerWidget.js';
import InputWidget from '../../widgets/InputWidget.js';
import SelectWidget from '../../widgets/SelectWidget.js';
import Radio from 'backbone.radio';


const ExpenseFormView = Mn.View.extend({
    behaviors: [FormBehavior],
    template: require('./templates/ExpenseFormView.mustache'),
	regions: {
        'category': '.category',
		'date': '.date',
		'type_id': '.type_id',
		'description': '.description',
		'ht': '.ht',
		'tva': '.tva',
    },
    // Bubble up child view events
    //
    childViewTriggers: {
        'change': 'data:modified',
    },
    initialize(){
        var channel = Radio.channel('config');
        if (this.getOption('tel')){
            this.type_options = channel.request(
                'get:options',
                'expensetel_types',
            );
        }else{
            this.type_options = channel.request(
                'get:options',
                'expense_types',
            );
            this.categories = channel.request(
                'get:options',
                'categories',
            );
        }
        this.today = channel.request(
            'get:options',
            'today',
        );
    },
    onRender(){
        var view;
        if (this.getOption('tel')){
            view = new InputWidget({
                value: "1",
                field_name: 'category',
                type: 'hidden',
            });
        }else{
            view = new SelectWidget({
                value: this.model.get('category'),
                field_name: 'category',
                options: this.categories,
                id_key: 'value',
                title: "Catégorie",
            });
        }
        this.showChildView('category', view);

        view = new DatePickerWidget({
            date: this.model.get('date'),
            title: "Date",
            field_name: "date",
            default_value: this.today,
        });
        this.showChildView("date", view);

        view = new SelectWidget({
            value: this.model.get('type_id'),
            title: 'Type de frais',
            field_name: 'type_id',
            options: this.type_options,
            id_key: 'id',
        });
        this.showChildView('type_id', view);

        if (! this.getOption('tel')){
            view = new InputWidget({
                value: this.model.get('description'),
                title: 'Description',
                field_name: 'description'
            });
            this.showChildView('description', view);
        }

        view = new InputWidget({
            value: this.model.get('ht'),
            title: 'Montant HT',
            field_name: 'ht',
            addon: "€",
        });
        this.showChildView('ht', view);

        view = new InputWidget({
            value: this.model.get('tva'),
            title: 'Montant TVA',
            field_name: 'tva',
            addon: "€",
        });
        this.showChildView('tva', view);
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            add: this.getOption('add'),
        };
    }
});
export default ExpenseFormView;
