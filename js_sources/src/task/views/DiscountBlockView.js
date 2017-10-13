/*
 * File Name : DiscountBlockView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import DiscountModel from '../models/DiscountModel.js';
import DiscountCollectionView from './DiscountCollectionView.js';
import DiscountFormPopupView from './DiscountFormPopupView.js';
import ExpenseView from './ExpenseView.js';
import {displayServerSuccess, displayServerError} from '../../backbone-tools.js';

const DiscountBlockView = Mn.View.extend({
    tagName: 'div',
    className: 'form-section discount-group',
    template: require('./templates/DiscountBlockView.mustache'),
    regions: {
        'lines': '.lines',
        'modalRegion': '.modalregion',
        'expenses_ht': '.expenses_ht',
    },
    ui: {
        add_button: 'button.btn-add'
    },
    triggers: {
        "click @ui.add_button": "line:add"
    },
    childViewEvents: {
        'line:edit': 'onLineEdit',
        'line:delete': 'onLineDelete',
        'destroy:modal': 'render',
        'insert:percent': 'onInsertPercent',
    },
    initialize: function(options){
        this.collection = options['collection'];
        this.model = options['model'];
    },
    isEmpty: function(){
        return this.collection.length === 0;
    },
    onLineAdd: function(){
        var model = new DiscountModel();
        this.showDiscountLineForm(model, "Ajouter la remise", false);
    },
    onLineEdit: function(childView){
        this.showDiscountLineForm(childView.model, "Modifier la remise", true);
    },
    showDiscountLineForm: function(model, title, edit){
        var form = new DiscountFormPopupView(
                {
                    model: model,
                    title: title,
                    destCollection: this.collection,
                    edit: edit
                }
            );
        this.showChildView('modalRegion', form);
    },
    onDeleteSuccess: function(){
        displayServerSuccess("Vos données ont bien été supprimées");
    },
    onDeleteError: function(){
        displayServerError("Une erreur a été rencontrée lors de la " +
                           "suppression de cet élément");
    },
    onLineDelete: function(childView){
        var result = window.confirm(
            "Êtes-vous sûr de vouloir supprimer cette remise ?"
        );
        if (result){
            childView.model.destroy(
                {
                    success: this.onDeleteSuccess,
                    error: this.onDeleteError
                }
            );
        }
    },
    onInsertPercent: function(model){
        this.collection.insert_percent(model);
        this.getChildView('modalRegion').triggerMethod('modal:close')
    },
    isMoreSet: function(){
        var value = this.model.get('expenses_ht');
        if (value && (value != '0')){
            return true;
        }
        return false;
    },
    templateContext: function(){
        return {
            not_empty: ! this.isEmpty(),
            is_more_set: this.isMoreSet(),
        }
    },
    onRender: function(){
        if (! this.isEmpty()){
            this.showChildView(
                'lines',
                new DiscountCollectionView({collection: this.collection})
            );
        }
        this.showChildView(
            'expenses_ht',
            new ExpenseView({model: this.model})
        );

    }
});
export default DiscountBlockView;
