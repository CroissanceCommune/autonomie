/*
 * File Name : ExpenseCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import ExpenseModel from "./ExpenseModel.js";
import Radio from 'backbone.radio';

const ExpenseCollection = Bb.Collection.extend({
    /*
     *  Collection of expense lines
     */
    model: ExpenseModel,
    initialize(){
        this.on('remove', this.channelCall);
        this.on('sync', this.channelCall);
        this.on('reset', this.channelCall);
        this.on('add', this.channelCall);
    },
    channelCall: function(model){
        console.log("Triggering Channel call");
        var channel = Radio.channel('facade');
        channel.trigger('changed:line', model.get('category'));
    },
    url(){
        return AppOption['context_url'] + "/lines";
    },
    comparator: function( a, b ){
      /*
       * Sort the collection and place special lines at the end
       */
      var res = 0;
      if ( b.isSpecial() ){
        res = -1;
      }else if( a.isSpecial() ){
        res = 1;
      }else{
        var acat = a.get('category');
        var bcat = b.get('category');
        if ( acat < bcat ){
          res = -1;
        }else if ( acat > bcat ){
          res = 1;
        }
        if (res === 0){
          var adate = a.get('altdate');
          var bdate = a.get('altdate');
          if (adate < bdate){
            res = -1;
          } else if ( acat > bcat ){
            res = 1;
          }
        }
      }
      return res;
    },
    total_ht: function(category){
      /*
       * Return the total value
       */
      var result = 0;
      this.each(function(model){
        if (category != undefined){
          if (model.get('category') != category){
            return;
          }
        }
        result += model.getHT();
      });
      return result;
    },
    total_tva: function(category){
      /*
       * Return the total value
       */
      var result = 0;
      this.each(function(model){
        if (category != undefined){
          if (model.get('category') != category){
            return;
          }
        }
        result += model.getTva();
      });
      return result;
    },
    total: function(category){
      /*
       * Return the total value
       */
      var result = 0;
      this.each(function(model){
        if (category != undefined){
          if (model.get('category') != category){
            return;
          }
        }
        result += model.total();
      });
      return result;
    },
});
export default ExpenseCollection;
