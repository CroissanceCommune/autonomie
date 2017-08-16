/*
 * File Name : ExpenseKmModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import BaseModel from './BaseModel.js';

const ExpenseKmModel = BaseModel.extend({
    defaults:{
      category:null,
      start:"",
      end:"",
      description:""
    },
    initialize(options){
      if ((options['altdate'] === undefined)&&(options['date']!==undefined)){
        this.set('altdate', formatPaymentDate(options['date']));
      }
    },
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
      km: {
        required:true,
        // Match"es 19,6 19.65 but not 19.654"
        pattern:/^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
        msg:"doit être un nombre"
      }
    },
    getIndice(){
      /*
       *  Return the reference used for compensation of km fees
       */
      var elem = _.where(AppOptions['expensekm_types'], {value:this.get('type_id')})[0];
      if (elem === undefined){
        return 0;
      }
      return parseFloat(elem.amount);
    },
    total(){
      var km = this.getKm();
      var amount = this.getIndice();
      return km * amount;
    },
    getKm(){
      return parseFloat(this.get('km'));
    },
    getTypeOptions(){
      return AppOptions['expensekm_types'];
    }

});
export default ExpenseKmModel;
