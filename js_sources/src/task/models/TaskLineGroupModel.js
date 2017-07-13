/*
 * File Name : TaskLineGroupModel.js
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


const TaskLineGroupModel = Bb.Model.extend({
    initialize: function(){
        this.populate();
    },
    populate: function(){
        this.lines = new TaskLineCollection(this.get('lines'));
        this.lines.url = this.url() + '/task_lines';
    },
    ht: function(){
        var res = 0;
        _.each(this.lines.models, function(line){
            res += line.ht()
        });
        return res;
    }
});
export default TaskLineGroupModel;
