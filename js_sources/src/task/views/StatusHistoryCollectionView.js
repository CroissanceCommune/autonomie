/*
 * File Name : StatusHistoryCollectionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';

const StatusHistoryItemView = Mn.View.extend({
    tagName: 'div',
    className: 'row',
    template: require('./templates/StatusHistoryItemView.mustache'),
    templateContext(){
        return {
            date: formatDate(this.model.get('date'))
        };
    }
});

const StatusHistoryCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    className: 'col-xs-12',
    childView: StatusHistoryItemView
});
export default StatusHistoryCollectionView;
