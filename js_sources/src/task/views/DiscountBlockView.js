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
import FormBehavior from '../behaviors/FormBehavior.js';
import DiscountModel from '../models/DiscountModel.js';
import DiscountCollectionView from './DiscountCollectionView.js';
import DiscountFormView from './DiscountFormView.js';
import InputWidget from './InputWidget.js';
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
    behaviors: [
        {
            behaviorClass: FormBehavior,
            errorMessage: "Vérifiez votre saisie"
        }
    ],
    ui: {
        add_button: 'button.btn-add'
    },
    triggers: {
        "click @ui.add_button": "line:add"
    },
    childViewEvents: {
        'line:edit': 'onLineEdit',
        'line:delete': 'onLineDelete',
        'change': 'onChildChange',
        'finish': 'onChildFinish'
    },
    initialize: function(options){
        this.collection = options['collection'];
        this.model = options['model'];
    },
    isEmpty: function(){
        return this.collection.length === 0;
    },
    onChildChange: function(attribute, value){
        console.log("Data modified");
        this.triggerMethod('data:modified', this, attribute, value);
    },
    onChildFinish: function(attribute, value){
        console.log("Data should be persisted");
        this.triggerMethod('data:persist', this, attribute, value);
    },
    onLineAdd: function(){
        var model = new DiscountModel();
        this.showDiscountLineForm(model, "Ajouter la remise", false);
    },
    onLineEdit: function(childView){
        this.showDiscountLineForm(childView.model, "Modifier la remise", true);
    },
    showDiscountLineForm: function(model, title, edit){
        var form = new DiscountFormView(
                {
                    model: model,
                    title: title,
                    destCollection: this.collection
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
    isMoreSet: function(){
        var value = this.model.get('expenses_ht');
        if (value){
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
export default DiscountBlockView;
