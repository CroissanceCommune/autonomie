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

const template = require('./templates/TaskLineGroupView.mustache');

const TaskLineGroupView = Mn.View.extend({
    template: template,
    regions: {
        lines: '.lines'
    },
    onRender: function(){
        this.showChildView('lines', new TaskLineCollectionView({collection: this.model.lines}));
    }
});
export default TaskLineGroupView;
