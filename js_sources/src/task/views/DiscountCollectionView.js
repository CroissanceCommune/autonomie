/*
 * File Name : DiscountCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import DiscountView from './DiscountView.js';

const DiscountCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    className: 'col-xs-12',
    childView: DiscountView,
    // Bubble up child view events
    childViewTriggers: {
        'edit': 'line:edit',
        'delete': 'line:delete'
    },
    collectionEvents: {
        'sync': 'render'
    },
});
export default DiscountCollectionView;
