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

const FacadeClass = Mn.Object.extend({
    channelName: 'facade',
    radioEvents: {
    },
    radioRequests: {
        'get:collection': 'getCollectionRequest',
        'get:totalmodel': 'getTotalModelRequest',
        // 'get:paymentcollection': 'getPaymentCollectionRequest',
        // 'get:totalmodel': 'getTotalModelRequest',
        // 'get:status_history_collection': 'getStatusHistory',
        // 'is:valid': "isDataValid",
        // 'get:attachments': 'getAttachments',
    },
    loadModels(form_datas){
        this.datas = form_datas;
        this.models = {};
        this.collections = {};
        this.totalmodel = new TotalModel();

        var internal = form_datas['internal'];

        var lines = internal['lines'];
        this.collections['internal_lines'] = new ExpenseCollection(lines);
        var kmlines = internal['kmlines'];
        this.collections['internal_kmlines'] = new ExpenseKmCollection(lines);

        var activity = form_datas['activity'];
        var lines = activity['lines'];
        this.collections['activity_lines'] = new ExpenseCollection(lines);
        var kmlines = activity['kmlines'];
        this.collections['activity_kmlines'] = new ExpenseKmCollection(lines);

        this.computeTotals();
    },
    computeTotals(){
        var internal_ht = this.collections['internal_lines'].total_ht();
        var internal_tva = this.collections['internal_lines'].total_tva();
        var internal_total = this.collections['internal_lines'].total_ttc();
        var internal_km = this.collections['internal_kmlines'].total_km();
        var internal_km_total = this.collections['internal_kmlines'] .total();
        var internal_ttc = internal_total + internal_km_total;

        var activity_ht = this.collections['activity_lines'].total_ht();
        var activity_tva = this.collections['activity_lines'].total_tva();
        var activity_total = this.collections['activity_lines'].total_ttc();
        var activity_km = this.collections['activity_kmlines'].total_km();
        var activity_km_total = this.collections['activity_kmlines'] .total();
        var activity_ttc = activity_total + activity_km_total;

        this.totalmodel.set({
            internal_ht: internal_ht,
            internal_tva: internal_tva,
            internal_total:internal_total,
            internal_km: internal_km,
            internal_km_total: internal_km_total,
            internal_ttc: internal_ttc,
            activity_ht: activity_ht,
            activity_tva: activity_tva,
            activity_total: activity_total,
            activity_km: activity_km,
            activity_ttc: activity_ttc,
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
