/*
 * File Name : Facade.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TotalModel from '../models/TotalModel.js';
import ExpenseCollection from '../models/ExpenseCollection.js';
import ExpenseKmCollection from '../models/ExpenseKmCollection.js';
import BookMarkCollection from '../models/BookMarkCollection.js';

const FacadeClass = Mn.Object.extend({
    channelName: 'facade',
    radioEvents: {
        "changed:line": "computeLineTotal",
        "changed:kmline": "computeKmLineTotal",
    },
    radioRequests: {
        'get:collection': 'getCollectionRequest',
        'get:totalmodel': 'getTotalModelRequest',
        'get:bookmarks': 'getBookMarks',
        // 'get:paymentcollection': 'getPaymentCollectionRequest',
        // 'get:totalmodel': 'getTotalModelRequest',
        // 'get:status_history_collection': 'getStatusHistory',
        // 'is:valid': "isDataValid",
        // 'get:attachments': 'getAttachments',
    },
    loadModels(form_datas, form_config){
        this.datas = form_datas;
        this.models = {};
        this.collections = {};
        this.totalmodel = new TotalModel();

        var lines = form_datas['lines'];
        this.collections['lines'] = new ExpenseCollection(lines);

        var kmlines = form_datas['kmlines'];
        this.collections['kmlines'] = new ExpenseKmCollection(kmlines);

        this.bookmarks = new BookMarkCollection(form_config.options.bookmarks);

        this.computeLineTotal();
        this.computeKmLineTotal();
    },
    getBookMarks(){
        return this.bookmarks;
    },
    computeLineTotal(category){
        /*
         * compute the line totals for the given category
         */
        var categories;
        if (_.isUndefined(category)){
            categories = ['1', '2'];
        } else {
            categories = [category]
        }
        var collection = this.collections['lines'];
        var datas = {}
        _.each(categories, function(category){
            datas['ht_' + category] = collection.total_ht(category);
            datas['tva_' + category] = collection.total_tva(category);
            datas['ttc_' + category] = collection.total(category);
        });
        this.totalmodel.set(datas);
        var channel = this.getChannel();
        _.each(categories, function(category){
            channel.trigger('change:lines_' + category);
        });

    },
    computeKmLineTotal(category){
        /*
         * Compute the kmline totals for the given category
         */
        var categories;
        if (_.isUndefined(category)){
            categories = ['1', '2'];
        } else {
            categories = [category]
        }
        var collection = this.collections['kmlines'];
        var datas = {}
        _.each(categories, function(category){
            datas['km_' + category] = collection.total_km(category);
            datas['km_ttc_' + category] = collection.total(category);
        });
        this.totalmodel.set(datas);

        var channel = this.getChannel();
        _.each(categories, function(category){
            channel.trigger('change:kmlines_' + category);
        });
    },
    getCollectionRequest(label){
        return this.collections[label];
    },
    getTotalModelRequest(){
        return this.totalmodel;
    },
});
const Facade = new FacadeClass();
export default Facade;
