/*
 * File Name : MainView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import CommonView from "./CommonView.js";
import RightBarView from "./RightBarView.js";
import TaskBlockView from './TaskBlockView.js';
import DiscountBlockView from './DiscountBlockView.js';
import StatusView from './StatusView.js';
import Radio from 'backbone.radio';
import { Modal } from 'bootstrap';

const template = require('./templates/MainView.mustache');

const MainView = Mn.View.extend({
    template: template,
    regions: {
        modalRegion: '#modalregion',
        common: '#common',
        tasklines: '#tasklines',
        discounts: '#discounts',
        rightbar: "#rightbar",
        footer: '#footer'
    },
    childViewEvents: {
        'status:change': 'onStatusChange',
    },
    initialize: function(options){
        this.channel = Radio.channel('facade');
    },
    showCommonBlock: function(datas){
        var model = this.channel.request('get:model', 'common');
        var view = new CommonView({model: model});
        this.showChildView('common', view);
    },
    showTaskGroupBlock: function(datas){
        var collection = this.channel.request('get:collection', 'task_groups');
        var view = new TaskBlockView({collection: collection});
        this.showChildView('tasklines', view);
    },
    showDiscountBlock(datas){
        var collection = this.channel.request('get:collection', 'discounts');
        var model = this.channel.request('get:model', 'common');
        var view = new DiscountBlockView({collection: collection, model: model});
        this.showChildView('discounts', view);
    },
    onRender: function() {
        if (_.indexOf(AppOption['form_options']['sections'], "common") != -1){
            this.showCommonBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "tasklines") != -1){
            this.showTaskGroupBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "discounts") != -1){
            this.showDiscountBlock();
        }

        var view = new RightBarView(
            {actions: AppOption['form_options']['actions']}
        );
        this.showChildView('rightbar', view);
    },
    onStatusChange: function(status, title, label, url){
        this.showChildView(
            'modalRegion',
            new StatusView({
                status: status,
                title: title,
                label: label,
                model: this.commonModel,
                url: url
            })
        );
    },
    onChildviewDestroyModal: function() {
    	this.getRegion('modalRegion').empty();
  	}
});
export default MainView;
