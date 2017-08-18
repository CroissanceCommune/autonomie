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
import ExpenseCollectionView from './ExpenseCollectionView.js';
import Radio from 'backbone.radio';
import { formatAmount } from '../../math.js';


const ExpenseTableView = Mn.View.extend({
    template: require('./templates/ExpenseTableView.mustache'),
    regions: {
       lines: {
           el: 'tbody',
           replaceElement: true
       }
    },
    ui:{
        add_btn: 'button.add',
        total_ht: '.total_ht',
        total_tva: '.total_tva',
        total_ttc: '.total_ttc'
    },
    triggers: {
        'click @ui.add_btn': 'line:add',
    },
    childViewTriggers: {
        'line:edit': 'line:edit',
        'line:delete': 'line:delete',
        'line:duplicate': 'line:duplicate',
        'bookmark:add': 'bookmark:add',
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
            'change:lines_' + this.categoryName,
            this.showTotals.bind(this)
        );
    },
    showTotals(){
        this.getUI("total_ht").html(
            formatAmount(this.totalmodel.get('ht_' + this.categoryName))
        );
        this.getUI("total_tva").html(
            formatAmount(this.totalmodel.get('tva_' + this.categoryName))
        );
        this.getUI("total_ttc").html(
            formatAmount(this.totalmodel.get('ttc_' +this.categoryName))
        );
    },
    templateContext(){
        return {
            category: this.getOption('category'),
            edit: this.getOption('edit'),
        };
    },
    onRender(){
        var view = new ExpenseCollectionView(
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
export default ExpenseTableView;
