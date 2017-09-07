/*
 * File Name : ExpenseKmCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import ExpenseKmModel from './ExpenseKmModel.js';
import Radio from 'backbone.radio';

const ExpenseKmCollection = Bb.Collection.extend({
    /*
     * Collection for expenses related to km fees
     */
    model: ExpenseKmModel,
    initialize(){
        this.on('remove', this.channelCall);
        this.on('sync', this.channelCall);
        this.on('reset', this.channelCall);
    },
    channelCall: function(model){
        var channel = Radio.channel('facade');
        channel.trigger('changed:kmline', model.get('category'));
    },
    url(){
        return AppOption['context_url'] + '/kmlines';
    },
    total_km: function(category){
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
        result += model.getKm();
      });
      return result;
    },
    total_tva: function(category){
        return 0;
    },
    total_ht: function(category){
        return this.total(category);
    },
    total: function(category){
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
    }
});
export default ExpenseKmCollection;
