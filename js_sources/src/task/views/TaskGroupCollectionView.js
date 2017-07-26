/*
 * File Name : TaskGroupCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TaskGroupView from './TaskGroupView.js';

const TaskGroupCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    childView: TaskGroupView,
    collectionEvents: {
        'change:reorder': 'render',
        'sync': 'render'
    },
    // Bubble up child view events
    childViewTriggers: {
        'edit': 'group:edit',
        'delete': 'group:delete',
        'catalog:insert': 'catalog:insert'
    },
    onChildviewOrderUp: function(childView){
        this.collection.moveUp(childView.model);
    },
    onChildviewOrderDown: function(childView){
        this.collection.moveDown(childView.model);
    },
});

export default TaskGroupCollectionView;
