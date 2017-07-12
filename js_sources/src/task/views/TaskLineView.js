/*
 * File Name : TaskLineView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
const template = require('./templates/TaskLineView.mustache');

const TaskLineView = Mn.View.extend({
    template: template,
    templateContext: function(){
        return {};
    }
});
export default TaskLineView;
