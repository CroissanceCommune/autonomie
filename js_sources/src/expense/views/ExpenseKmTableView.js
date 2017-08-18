/*
 * File Name : ExpenseKmTableView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import ExpenseKmCollectionView from './ExpenseKmCollectionView.js';
import Radio from 'backbone.radio';
import {formatAmount} from '../../math.js';


const ExpenseKmTableView = Mn.View.extend({
    template: require('./templates/ExpenseKmTableView.mustache'),
    regions: {
       lines: {
           el: 'tbody',
           replaceElement: true
       }
    },
    ui:{
        add_btn: 'button.add',
        total_km: '.total_km',
        total_ttc: '.total_ttc'
    },
    triggers: {
        'click @ui.add_btn': 'kmline:add',
    },
    childViewTriggers: {
        'kmline:edit': 'kmline:edit',
        'kmline:delete': 'kmline:delete',
        'kmline:duplicate': 'kmline:duplicate',
    },
    collectionEvents: {
        'change:category': 'render',
    },
    initialize(){
        var channel = Radio.channel('facade');
        this.totalmodel = channel.request('get:totalmodel');
        this.categoryName = this.getOption('category').value;
        this.listenTo(
            channel,
            'change:kmlines_' + this.categoryName,
            this.showTotals.bind(this)
        );
    },
    showTotals(){
        this.getUI("total_km").html(
            this.totalmodel.get('km_' + this.categoryName) + " km"
        );
        this.getUI("total_ttc").html(
            formatAmount(this.totalmodel.get('km_ttc_' + this.categoryName))
        );
    },
    templateContext(){
        return {
            category: this.getOption('category'),
            edit: this.getOption('edit'),
        };
    },
    onRender(){
        var view = new ExpenseKmCollectionView(
            {
                collection: this.collection,
                category: this.getOption('category'),
                edit: this.getOption('edit'),
            }
        );
        this.showChildView('lines', view);
    },
    onAttach(){
        this.showTotals();
    }
});
export default ExpenseKmTableView;
