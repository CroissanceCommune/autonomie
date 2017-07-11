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

var template = require("./templates/RightBarView.mustache");

const RightBarView = Mn.View.extend({
    regions: {
        container: ".child-container"
    },
    ui: {
        buttons: 'button',
    },
    events: {
        'click @ui.buttons': 'onButtonClick'
    },
    template: template,
    templateContext: function(){
        return {
            buttons: this.getOption('actions')['status']
        }
    },
    onButtonClick: function(event){
        let target = $(event.target);
        console.log(target);
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
    }
});
export default RightBarView;
