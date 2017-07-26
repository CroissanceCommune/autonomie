/*
 * File Name : TaskGroupModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import Bb from 'backbone';
import TaskLineCollection from './TaskLineCollection.js';
import {ajax_call} from '../../tools.js';


const TaskGroupModel = Bb.Model.extend({
    props: [
        'id',
        'order',
        'title',
        'description',
        'lines',
        'task_id',
    ],
    constructor: function() {
        arguments[0] = _.pick(arguments[0], this.props);
        Bb.Model.apply(this, arguments);
    },
    initialize: function(){
        this.populate();
        this.on('change:id', this.populate.bind(this));
    },
    populate: function(){
        if (this.get('id')){
            this.lines = new TaskLineCollection(this.get('lines'));
            this.lines.url = this.url() + '/task_lines';
        }
    },
    ht: function(){
        var res = 0;
        _.each(this.lines.models, function(line){
            res += line.ht()
        });
        return res;
    },
    updateLines: function(result){
        this.fetch({success: this.populate.bind(this)});
    },
    load_from_catalog: function(sale_product_ids){
        var serverRequest = ajax_call(
            this.url() + '?action=load_from_catalog',
            {sale_product_ids: sale_product_ids},
            'POST'
        );
        serverRequest.then(this.updateLines.bind(this));
    },
    loadProductGroup: function(sale_product_group_datas){
        this.set('title', sale_product_group_datas.title);
        this.set('description', sale_product_group_datas.description);
    }
});
export default TaskGroupModel;
