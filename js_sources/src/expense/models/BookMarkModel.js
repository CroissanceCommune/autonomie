/*
 * File Name : BookMarkModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import Radio from 'backbone.radio';

const BookMarkModel = Bb.Model.extend({
    initialize: function(options){
        var type_id = options['type_id'];
        if (! _.isUndefined(type_id)){
            this.set('type', this.getType(type_id));
        }
        var config = Radio.channel('config');
        this.expense_types = config.request('get:option', 'expense_types');
        this.expensetel_types = this.config.request('get:options', 'expensetel_types');
    },
    getType: function(type_id){
        return _.find(
            this.expense_types,
            function(type){
                return type['value'] == type_id;
            }
        );
    },
    isSpecial:function(){
      /*
       * return True if this expense is a special one (related to phone)
       */
      return this.getTypeOption(this.expensetel_types) !== undefined;
    },
});
export default BookMarkModel;
