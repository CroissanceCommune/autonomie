/*
 * File Name : ExpenseTableView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';


const ExpenseTableView = Mn.View.extend({
    template: require('./templates/ExpenseTableView.mustache'),
    templateContext(){
        return {};
    }
});
export default ExpenseTableView;
