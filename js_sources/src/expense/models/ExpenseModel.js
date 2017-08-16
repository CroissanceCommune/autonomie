/*
 * File Name : ExpenseModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import BaseModel from './BaseModel.js';

const ExpenseModel = BaseModel.extend({
    defaults:{
      category: null,
      description:"",
      ht:null,
      tva:null
    },
    // Constructor dynamically add a altdate if missing
    // (altdate is used in views for jquery datepicker)
    initialize(options){
      if ((options['altdate'] === undefined)&&(options['date']!==undefined)){
        this.set('altdate', formatPaymentDate(options['date']));
      }
    },
    // Validation rules for our model's attributes
    validation:{
      category: {
        required:true,
        msg:"est requise"
      },
      type_id:{
        required:true,
        msg:"est requis"
      },
      date: {
        required:true,
        pattern:/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
        msg:"est requise"
      },
      ht: {
        required:true,
        // Match"es 19,6 19.65 but not 19.654"
        pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
        msg:"doit être un nombre"
      },
      tva: {
        required:true,
        pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
        msg:"doit être un nombre"
      }
    },
    total: function(){
      var total = this.getHT() + this.getTva();
      return total;
    },
    getTva:function(){
      var result = parseFloat(this.get('tva'));
      if (this.isSpecial()){
        var percentage = this.getTypeOption(AppOptions['expensetel_types']).percentage;
        result = getPercent(result, percentage);
      }
      return result
    },
    getHT:function(){
      var result = parseFloat(this.get('ht'));
      if (this.isSpecial()){
        var percentage = this.getTypeOption(AppOptions['expensetel_types']).percentage;
        result = getPercent(result, percentage);
      }
      return result
    },
    isSpecial:function(){
      /*
       * return True if this expense is a special one (related to phone)
       */
      return this.getTypeOption(AppOptions['expensetel_types']) !== undefined;
    },
    hasNoType: function(){
      var isnottel = _.isUndefined(this.getTypeOption(AppOptions['expensetel_types']));
      var isnotexp = _.isUndefined(this.getTypeOption(AppOptions['expense_types']));
      if (isnottel && isnotexp){
        return true;
      }else{
        return false;
      }
    },
    getTypeOptions: function(){
      var arr;
      if (this.isSpecial()){
        arr = AppOptions['expensetel_types'];
      }else{
        arr = AppOptions['expense_types'];
      }
      return arr;
    }
});
export default ExpenseModel;
