/*
 * File Name : ExpenseKmFormView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import ModalFormBehavior from '../../base/behaviors/ModalFormBehavior.js';
import DatePickerWidget from '../../widgets/DatePickerWidget.js';
import InputWidget from '../../widgets/InputWidget.js';
import SelectWidget from '../../widgets/SelectWidget.js';
import Radio from 'backbone.radio';


const ExpenseKmFormView = Mn.View.extend({
    behaviors: [ModalFormBehavior],
    template: require('./templates/ExpenseKmFormView.mustache'),
	regions: {
        'category': '.category',
		'date': '.date',
		'type_id': '.type_id',
		'start': '.start',
		'end': '.end',
		'km': '.km',
		'description': '.description',
    },
    // Bubble up child view events
    //
    childViewTriggers: {
        'change': 'data:modified',
    },
    initialize(){
        var channel = Radio.channel('config');
        this.type_options = channel.request(
            'get:options',
            'expensekm_types',
        );
        this.categories = channel.request(
            'get:options',
            'categories',
        );
        this.today = channel.request(
            'get:options',
            'today',
        );
    },
    refreshForm(){
        var view = new SelectWidget({
            value: this.model.get('category'),
            field_name: 'category',
            options: this.categories,
            id_key: 'value',
            title: "Catégorie",
        });
        this.showChildView('category', view);

        view = new DatePickerWidget({
            date: this.model.get('date'),
            title: "Date",
            field_name: "date",
            current_year: true,
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

        view = new InputWidget({
            value: this.model.get('start'),
            title: 'Point de départ',
            field_name: 'start',
        });
        this.showChildView('start', view);

        view = new InputWidget({
            value: this.model.get('end'),
            title: "Point d'arrivée",
            field_name: 'end',
        });
        this.showChildView('end', view);

        view = new InputWidget({
            value: this.model.get('km'),
            title: "Nombre de kilomètres",
            field_name: 'km',
            addon: "km",
        });
        this.showChildView('km', view);

        view = new InputWidget({
            value: this.model.get('description'),
            title: 'Description',
            description: "Le cas échéant, indiquer la prestation liée à ces dépenses",
            field_name: 'description'
        });
        this.showChildView('description', view);
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
        };
    },
    onRender(){
        this.refreshForm();
    }
});
export default ExpenseKmFormView;
