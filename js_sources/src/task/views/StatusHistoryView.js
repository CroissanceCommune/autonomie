/*
 * File Name : StatusHistoryView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Radio from 'backbone.radio';
import StatusHistoryCollectionView from './StatusHistoryCollectionView.js';


const StatusHistoryView = Mn.View.extend({
    template: require('./templates/StatusHistoryView.mustache'),
    regions: {
        comments: '.comments'
    },
    onRender(){
        var collection = this.getOption('collection');
        this.showChildView(
            "comments",
            new StatusHistoryCollectionView({collection: collection})
        );
    }
});
export default StatusHistoryView;
