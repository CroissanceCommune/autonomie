/*
 * File Name : TaskGroupTotalView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { formatAmount } from "../../math.js";
import LabelRowWidget from './LabelRowWidget.js';

const TaskGroupTotalView = Mn.View.extend({
    template: require('./templates/LineContainerView.mustache'),
    regions: {
        line: {
            el: '.line',
            replaceElement: true
        }
    },
    collectionEvents: {
        'change': 'render',
        'remove': 'render',
        'add': 'render',
    },
    onRender: function(){
        var values = formatAmount(this.collection.ht(), false);
        var view = new LabelRowWidget(
            {
                label: 'Sous total HT',
                values: values
            }
        );
        this.showChildView('line', view);
    }
});
export default TaskGroupTotalView;
