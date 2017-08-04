/*
 * File Name : TaskBlockView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TaskGroupModel from '../models/TaskGroupModel.js';
import TaskGroupCollectionView from './TaskGroupCollectionView.js';
import TaskGroupFormView from './TaskGroupFormView.js';
import {displayServerSuccess, displayServerError} from '../../backbone-tools.js';
import ErrorView from './ErrorView.js';

const TaskBlockView = Mn.View.extend({
    template: require('./templates/TaskBlockView.mustache'),
    tagName: 'div',
    className: 'form-section',
    regions: {
        errors: '.group-errors',
        container: '.group-container',
        modalRegion: ".group-modalregion",
    },
    ui: {
        add_button: 'button.add'
    },
    triggers: {
        "click @ui.add_button": "group:add"
    },
    childViewEvents: {
        'group:edit': 'onGroupEdit',
        'group:delete': 'onGroupDelete',
        'catalog:insert': 'onCatalogInsert',
    },
    collectionEvents: {
        'change': 'hideErrors'
    },
    initialize: function(options){
        this.collection = options['collection'];
        this.listenTo(this.collection, 'validated:invalid', this.showErrors);
        this.listenTo(this.collection, 'validated:valid', this.hideErrors.bind(this));
    },
    showErrors(model, errors){
        this.detachChildView('errors');
        this.showChildView('errors', new ErrorView({errors: errors}));
        this.$el.addClass('error');
    },
    hideErrors(model){
        this.detachChildView('errors');
        this.$el.removeClass('error');
    },
    onDeleteSuccess: function(){
        displayServerSuccess("Vos données ont bien été supprimées");
    },
    onDeleteError: function(){
        displayServerError("Une erreur a été rencontrée lors de la " +
                           "suppression de cet élément");
    },
    onGroupDelete: function(childView){
        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cet ouvrage ?");
        if (result){
            childView.model.destroy(
                {
                    success: this.onDeleteSuccess,
                    error: this.onDeleteError
                }
            );
        }
    },
    onGroupEdit: function(childView){
        this.showTaskGroupForm(childView.model, "Modifier cet ouvrage");
    },
    onGroupAdd: function(){
        var model = new TaskGroupModel({
            order: this.collection.getMaxOrder() + 1
        });
        this.showTaskGroupForm(model, "Ajouter un ouvrage");
    },
    onEditGroup: function(childView){
        var model = childView.model;
        this.showTaskGroupForm(model, "Modifier cet ouvrage");
    },
    showTaskGroupForm: function(model, title){
        var form = new TaskGroupFormView(
            {
                model: model,
                title: title,
                destCollection: this.collection
            }
        );
        this.showChildView('modalRegion', form);
    },
    onCatalogInsert: function(sale_product_group_ids){
        this.collection.load_from_catalog(sale_product_group_ids);
        this.getChildView('modalRegion').triggerMethod('modal:close')
    },
    onChildviewDestroyModal: function() {
        this.detachChildView('modalRegion');
    	this.getRegion('modalRegion').empty();
  	},
    onRender: function(){
        this.showChildView(
            'container',
            new TaskGroupCollectionView(
                {collection: this.collection}
            )
        );
    }
});
export default TaskBlockView;
