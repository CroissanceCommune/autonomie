/*
 * File Name : TaskLineCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TaskLineView from './TaskLineView.js';

const TaskLineCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    className: 'col-xs-12',
    childView: TaskLineView,
    sort: true,
    collectionEvents: {
        'change:reorder': 'render'
    },
    childViewEvents: {
        'change:order:up': 'onOrderUp',
        'change:order:down': 'onOrderDown'
    },
    onOrderUp: function(childView){
        this.collection.moveUp(childView.model);
    },
    onOrderDown: function(childView){
        this.collection.moveDown(childView.model);
    },
    onRender: function(){
        console.log("Rendering");
    }
});
export default TaskLineCollectionView;
