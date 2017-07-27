/*
 * File Name : Facade.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';

import CommonModel from "../models/CommonModel.js";
import TaskGroupCollection from '../models/TaskGroupCollection.js';
import DiscountCollection from '../models/DiscountCollection.js';

const FacadeClass = Mn.Object.extend({
    channelName: 'facade',
    ht: 5,
    radioEvents: {
        'update:model': 'onModelUpdated',
    },
    radioRequests: {
        'get:total_ht': 'ht',
        'get:model': 'getModelRequest',
        'get:collection': 'getCollectionRequest',
    },
    initialize: function(options){
        this.models = {};
        this.collections = {};
    },
    loadModels: function(datas){
        this.models['common'] = new CommonModel(datas);
        this.models['common'].url = AppOption['context_url'];

        var lines = datas['line_groups'];
        this.collections['task_groups'] = new TaskGroupCollection(lines);

        var discounts = datas['discounts'];
        this.collections['discounts'] = new DiscountCollection(discounts);
    },
    getModelRequest: function(label){
        return this.models[label];
    },
    getCollectionRequest: function(label){
        return this.collections[label];
    },
    onModelUpdated: function(){
        console.log("onModelUpdated");
    },
    ht: function(){
        console.log("Requesting the ht");
        return this.ht;
    }
});
const Facade = new FacadeClass();
export default Facade;
