/*
 * File Name : ExpenseCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import ExpenseView from './ExpenseView.js';
import ExpenseEmptyView from './ExpenseEmptyView.js';

const ExpenseCollectionView = Mn.CollectionView.extend({
    tagName: 'tbody',
    // Bubble up child view events
    childViewTriggers: {
        'edit': 'line:edit',
        'delete': 'line:delete',
        'bookmark': 'bookmark:add',
        'duplicate': 'line:duplicate',
    },
    childView: ExpenseView,
    emptyView: ExpenseEmptyView,
    emptyViewOptions(){
        return {
            colspan: 6,
            edit: this.getOption('edit'),
        };
    },
    childViewOptions(){
        return {edit: this.getOption('edit')};
    },
    filter (child, index, collection) {
        if (child.get('category') == this.getOption('category').value){
            return true;
        } else {
            return false;
        }
    }
});
export default ExpenseCollectionView;
