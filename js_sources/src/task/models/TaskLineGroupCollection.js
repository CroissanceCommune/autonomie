/*
 * File Name : TaskLineGroupCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import TaskLineGroupModel from './TaskLineGroupModel.js';


const TaskLineGroupCollection = Bb.Collection.extend({
    model: TaskLineGroupModel,
    url: function(){
        return AppOption['context_url'] + '/' + 'task_line_groups';
    }
});
export default TaskLineGroupCollection;
