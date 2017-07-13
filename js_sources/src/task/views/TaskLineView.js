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
import _ from 'underscore';
import Mn from 'backbone.marionette';
import { formatAmount } from '../../math.js';
const template = require('./templates/TaskLineView.mustache');

const TaskLineView = Mn.View.extend({
    tagName: 'tr',
    template: template,
    getTvaLabel: function(){
        let res = "";
        let current_value = this.model.get('tva');
        console.log(current_value);
        _.each(AppOption['form_options']['tva_options'], function(tva){
            if (tva.value == current_value){
                res = tva.name;
            }
        });
        return res
    },
    templateContext: function(){
        console.log(this.getTvaLabel());
        return {
            ht: formatAmount(this.model.ht()),
            tva_label: this.getTvaLabel()
        };
    }
});
export default TaskLineView;
