/*
 * File Name : RightBarView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import $ from 'jquery';
import Mn from 'backbone.marionette';
import ActionCollection from '../models/ActionCollection.js';
import ActionListView from './ActionListView.js';
import { formatAmount } from '../../math.js';
import Radio from 'backbone.radio';
import StatusHistoryView from './StatusHistoryView.js';

var template = require("./templates/RightBarView.mustache");

const RightBarView = Mn.View.extend({
    regions: {
        container: ".child-container",
        status_history: '.status_history',
    },
    ui: {
        buttons: 'button',
    },
    events: {
        'click @ui.buttons': 'onButtonClick'
    },
    modelEvents: {
        'change': 'render'
    },
    template: template,
    templateContext: function(){
        return {
            buttons: this.getOption('actions')['status'],
            ttc: formatAmount(this.model.get('ttc'), true),
            ht: formatAmount(this.model.get('ht', true)),
            ht_before: formatAmount(this.model.get('ht_before_discounts'), false),
            tvas: this.model.tva_labels(),
        }
    },
    onButtonClick: function(event){
        let target = $(event.target);
        let status = target.data('status');
        let title = target.data('title');
        let label = target.data('label');
        let url = target.data('url');
        this.triggerMethod('status:change', status, title, label, url);
    },
    onRender: function(){
        const action_collection = new ActionCollection(
            this.getOption('actions')['others']
        );
        this.showChildView(
            'container',
            new ActionListView({collection: action_collection})
        );
        var collection = Radio.channel('facade').request(
            'get:status_history_collection'
        );
        if (collection.models.length > 0){
            this.showChildView(
                'status_history',
                new StatusHistoryView({collection: this.collection})
            );
        }
    }
});
export default RightBarView;
