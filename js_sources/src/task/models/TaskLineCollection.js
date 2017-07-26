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
import _ from 'underscore';
import Bb from 'backbone';
import TaskLineModel from './TaskLineModel.js';

const TaskLineCollection = Bb.Collection.extend({
    model: TaskLineModel,
    comparator: 'order',
    initialize: function(options) {
        this.on('change:reorder', this.updateModelOrder);
        this.updateModelOrder(false);
    },
    updateModelOrder: function(sync){
        var sync = sync || true;
        this.each(function(model, index) {
            model.set('order', index);
            if (sync){
                model.save(
                    {'order': index},
                    {patch: true},
                );
            }
        });

    },
    getMinOrder: function(){
        if (this.models.length == 0){
            return 0
        }
        let first_model = _.min(
            this.models,
            function(model){return model.get('order')}
        );
        return first_model.get('order');
    },
    getMaxOrder: function(){
        if (this.models.length == 0){
            return 0
        }
        let last_model = _.max(
            this.models,
            function(model){return model.get('order')}
        );
        return last_model.get('order');
    },
    moveUp: function(model) { // I see move up as the -1
        var index = this.indexOf(model);
        if (index > 0) {
            this.models.splice(index - 1, 0, this.models.splice(index, 1)[0]);
            this.trigger('change:reorder');
        }
    },
    moveDown: function(model) {
        // I see move up as the -1
        var index = this.indexOf(model);
        if (index < this.models.length) {
            this.models.splice(index + 1, 0, this.models.splice(index, 1)[0]);
            this.trigger('change:reorder');
        }
    }
});
export default TaskLineCollection;
