/*
 * File Name : PaymentLineCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import PaymentLineView from './PaymentLineView.js';

const PaymentLineCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    childView: PaymentLineView,
    collectionEvents: {
        'change:reorder': 'render',
    },
    childViewTriggers: {
        'edit': 'line:edit',
        'delete': 'line:delete'
    },
    childViewOptions: function(model){
        let edit = this.getOption('edit');
        return {
            show_date: this.getOption('show_date'),
            edit: edit
        };
    },
    onChildviewOrderUp: function(childView){
        this.collection.moveUp(childView.model);
    },
    onChildviewOrderDown: function(childView){
        this.collection.moveDown(childView.model);
    },
});
export default PaymentLineCollectionView;
