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
    onRender: function(){
        this.showChildView(
            'lines',
            new TaskLineCollectionView({collection: this.model.lines})
        );
    },
    showAddForm: function(){
        var model = new TaskLineModel({
            task_id: this.model.get('id'),
            order: this.model.lines.getMaxOrder() + 1
        });
        this.showTaskLineEditForm(model, "Ajouter une prestation");
    },
    showTaskLineEditForm: function(model, title){
        var form = new TaskLineEditView({model: model, title: title});
        this.showChildView('modalRegion', form);
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
