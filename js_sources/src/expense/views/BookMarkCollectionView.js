/*
 * File Name : BookMarkCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { formatAmount } from '../../math.js';

const BookMarkView = Mn.View.extend({
    tagName: 'div',
    className: 'row bookmark-line',
    template: require('./templates/BookMarkView.mustache'),
    ui: {
        delete_btn: '.delete',
        insert_btn: '.insert',
    },
    triggers: {
        'click @ui.delete_btn': 'bookmark:delete',
        'click @ui.insert_btn': 'bookmark:insert',
    },
    templateContext(){
        var typelabel = this.model.getTypeLabel();
        return {
            ht: formatAmount(this.model.get('ht')),
            tva: formatAmount(this.model.get('tva')),
            typelabel: typelabel,
        }
    }
});

const BookMarkCollectionView = Mn.CollectionView.extend({
    childView: BookMarkView,
    childViewTriggers: {
        'bookmark:delete': 'bookmark:delete',
        'bookmark:insert': 'bookmark:insert',
    }
});
export default BookMarkCollectionView;
