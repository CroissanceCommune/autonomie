/*
 * File Name : TaskGroupView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TaskLineCollectionView from './TaskLineCollectionView.js';
import TaskLineFormView from './TaskLineFormView.js';
import TaskLineModel from "../models/TaskLineModel.js";
import TaskGroupTotalView from './TaskGroupTotalView.js';
import { formatAmount } from '../../math.js';
import {displayServerSuccess, displayServerError} from '../../backbone-tools.js';

const template = require('./templates/TaskGroupView.mustache');

const TaskGroupView = Mn.View.extend({
    tagName: 'div',
    className: 'taskline-group row',
    template: template,
    regions: {
        lines: '.lines',
        modalRegion: ".modalregion",
        total: '.subtotal'
    },
    ui: {
        btn_add: ".btn-add",
        up_button: 'button.up',
        down_button: 'button.down',
        edit_button: 'button.edit',
        delete_button: 'button.delete'
    },
    triggers: {
        'click @ui.up_button': 'order:up',
        'click @ui.down_button': 'order:down',
        'click @ui.edit_button': 'edit',
        'click @ui.delete_button': 'delete'
    },
    events: {
        "click @ui.btn_add": "onLineAdd"
    },
    childViewEvents: {
        'line:edit': 'onLineEdit',
        'line:delete': 'onLineDelete',
        'catalog:insert': 'onCatalogInsert',
        'destroy:modal': 'render'
    },
    initialize: function(options){
        // Collection of task lines
        this.collection = this.model.lines;
        this.listenTo(this.collection, 'sync', this.showLines.bind(this));
    },
    isEmpty: function(){
        return this.model.lines.length === 0;
    },
    showLines(){
        /*
         * Show lines if it's not done yet
         */
        console.log("TaskGroupView.showLines");
        if (!_.isNull(this.getChildView('lines'))){
            console.log("  + Doing it")
            this.showChildView(
                'lines',
                new TaskLineCollectionView({collection: this.collection})
            );
        }
    },
    onRender: function(){
        if (! this.isEmpty()){
            this.showLines();
            this.showChildView(
                'total',
                new TaskGroupTotalView({collection: this.collection})
            );
        }
    },
    onLineEdit: function(childView){
        this.showTaskLineForm(childView.model, "Modifier la prestation", true);
    },
    onLineAdd: function(){
        var model = new TaskLineModel({
            task_id: this.model.get('id'),
            order: this.collection.getMaxOrder() + 1,
        });
        this.showTaskLineForm(model, "Ajouter une prestation", false);
    },
    showTaskLineForm: function(model, title, edit){
        var form = new TaskLineFormView(
            {
                model: model,
                title: title,
                destCollection: this.collection,
                edit: edit
            });
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
        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cette prestation ?");
        if (result){
            childView.model.destroy(
                {
                    success: this.onDeleteSuccess,
                    error: this.onDeleteError
                }
            );
        }
    },
    onCatalogInsert: function(sale_product_ids){
        this.collection.load_from_catalog(sale_product_ids);
        this.getChildView('modalRegion').triggerMethod('modal:close')
    },
    onChildviewDestroyModal: function() {
    	this.getRegion('modalRegion').empty();
  	},
    templateContext: function(){
        let min_order = this.model.collection.getMinOrder();
        let max_order = this.model.collection.getMaxOrder();
        let order = this.model.get('order');
        return {
            not_is_empty: !this.isEmpty(),
            total_ht: formatAmount(this.model.ht(), false),
            is_not_first: order != min_order,
            is_not_last: order != max_order
        }
    }
});
export default TaskGroupView;
