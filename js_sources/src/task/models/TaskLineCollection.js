/*
 * File Name : TaskLineCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import TaskLineModel from './TaskLineModel.js';

const TaskLineCollection = Bb.Collection.extend({
    model: TaskLineModel
});
export default TaskLineCollection;
