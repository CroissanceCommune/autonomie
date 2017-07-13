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
import CommonModel from "../models/CommonModel.js";
import TaskLineGroupCollection from '../models/TaskLineGroupCollection.js';
import TaskLineGroupCollectionView from './TaskLineGroupCollectionView.js';
import StatusView from './StatusView.js';
import { Modal } from 'bootstrap';

const template = require('./templates/MainView.mustache');

const MainView = Mn.View.extend({
    template: template,
    regions: {
        modalRegion: '#modalregion',
        common: '#common',
        tasklines: '#tasklines',
        rightbar: "#rightbar",
        footer: '#footer'
    },
    childViewEvents: {
        'status:change': 'onStatusChange',
    },
    onRender: function() {
        this.commonModel = new CommonModel(
            this.getOption('datas')
        );
        this.commonModel.url = AppOption['context_url'];

        if (_.indexOf(AppOption['form_options']['sections'], "common") != -1){
            this.showChildView(
                'common',
                new CommonView({model: this.commonModel})
            );
        }
        if (_.indexOf(AppOption['form_options']['sections'], "tasklines") != -1){
            this.task_line_group_collection = new TaskLineGroupCollection(this.getOption('datas')['line_groups']);
            this.showChildView(
                'tasklines',
                new TaskLineGroupCollectionView({collection: this.task_line_group_collection})
            );
        }

        this.showChildView(
            'rightbar',
            new RightBarView({actions: AppOption['form_options']['actions']})
        );
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
