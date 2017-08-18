/*
 * File Name : ExpenseEmptyView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';

const ExpenseEmptyView = Mn.View.extend({
    template: require('./templates/ExpenseEmptyView.mustache'),
    templateContext(){
        var colspan = this.getOption('colspan');
        if (this.getOption('edit')){
            colspan += 1;
        }
        return {
            colspan: colspan
        };
    }
});
export default ExpenseEmptyView;
