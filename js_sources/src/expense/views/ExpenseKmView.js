/*
 * File Name : ExpenseView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { formatAmount } from '../../math.js';

const ExpenseKmView = Mn.View.extend({
    tagName: 'tr',
    template: require('./templates/ExpenseKmView.mustache'),
    modelEvents: {
        'change': 'render'
    },
    ui: {
        edit: 'button.edit',
        delete: 'button.delete',
        duplicate: 'button.duplicate',
    },
    triggers: {
        'click @ui.edit': 'edit',
        'click @ui.delete': 'delete',
        'click @ui.duplicate': 'duplicate',
    },
    templateContext(){
        var total = this.model.total();
        var typelabel = this.model.getTypeLabel();
        return {
            edit: this.getOption('edit'),
            typelabel:typelabel,
            total:formatAmount(total),
        };
    }
});
export default ExpenseKmView;
