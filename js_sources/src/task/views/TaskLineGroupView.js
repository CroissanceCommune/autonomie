/*
 * File Name : TaskLineGroupView.js
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
import TaskLineEditView from './TaskLineEditView.js';
import TaskLineModel from "../models/TaskLineModel.js";
import { formatAmount } from '../../math.js';
import {displayServerSuccess, displayServerError} from '../../backbone-tools.js';

const template = require('./templates/TaskLineGroupView.mustache');

const TaskLineGroupView = Mn.View.extend({
    tagName: 'div',
    className: 'taskline-group row',
    template: template,
    regions: {
        lines: '.tasklines',
        modalRegion: ".modalregion",
    },
    ui: {
        btn_add: ".btn-add"
    },
    events: {
        "click @ui.btn_add": "showAddForm"
    },
    childViewEvents: {
        'line:edit': 'onLineEdit',
        'line:delete': 'onLineDelete',
    },
    onRender: function(){
        this.showChildView(
            'lines',
            new TaskLineCollectionView({collection: this.model.lines})
        );
    },
    onLineEdit: function(childView){
        console.log("Line edit");
        this.showTaskLineForm(childView.model, "Modifier la prestation");
    },
    showAddForm: function(){
        var model = new TaskLineModel({
            task_id: this.model.get('id'),
            order: this.model.lines.getMaxOrder() + 1,
        });
        this.showTaskLineForm(model, "Ajouter une prestation");
    },
    showTaskLineForm: function(model, title){
        var form = new TaskLineEditView(
            {
                model: model,
                title: title,
                destCollection: this.model.lines
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
        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cet élément ?");
        if (result){
            childView.model.destroy(
                {
                    success: this.onDeleteSuccess,
                    error: this.onDeleteError
                }
            );
        }
    },
    onChildviewDestroyModal: function() {
    	this.getRegion('modalRegion').empty();
  	},
    templateContext: function(){
        return {
            total_ht: formatAmount(this.model.ht())
        }
    }
});
export default TaskLineGroupView;
