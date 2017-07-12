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
import Bb from 'backbone';
import TaskLineCollection from './TaskLineCollection.js';


const TaskLineGroupModel = Bb.Model.extend({
    initialize: function(){
        this.populate();
    },
    populate: function(){
        console.log("Populating the TaskLineGroupModel");
        console.log(this.get('lines'));
        this.lines = new TaskLineCollection(this.get('lines'));
        console.log(this.lines);
    }
});
export default TaskLineGroupModel;
