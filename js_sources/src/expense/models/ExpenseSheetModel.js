/*
 * File Name : ExpenseSheetModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
const ExpenseSheetModel = Bb.Model.extend({
    urlRoot:"/expenses/",
    initialize: function(options){
      this.lines = new ExpenseLineCollection(options['lines']);
      this.lines.url = this.urlRoot + this.id + "/lines";
      this.kmlines = new ExpenseKmCollection(options['kmlines']);
      this.kmlines.url = this.urlRoot + this.id + "/kmlines";
    }
});
export default ExpenseSheetModel;
