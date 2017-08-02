/*
 * File Name : MainView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Radio from 'backbone.radio';

import CommonView from "./CommonView.js";
import TaskBlockView from './TaskBlockView.js';
import DiscountBlockView from './DiscountBlockView.js';

import RightBarView from "./RightBarView.js";
import StatusView from './StatusView.js';
import HtBeforeDiscountsView from './HtBeforeDiscountsView.js';
import TotalView from './TotalView.js';
import NotesBlockView from './NotesBlockView.js';
import BootomActionView from './BootomActionView.js';
import PaymentConditionBlockView from './PaymentConditionBlockView.js';
import PaymentBlockView from './PaymentBlockView.js';
import LoginView from './LoginView.js';

const template = require('./templates/MainView.mustache');

const MainView = Mn.View.extend({
    template: template,
    regions: {
        modalRegion: '#modalregion',
        common: '#common',
        tasklines: '#tasklines',
        discounts: '#discounts',
        rightbar: "#rightbar",
        ht_before_discounts: '.ht_before_discounts',
        totals: '.totals',
        notes: '.notes',
        payment_conditions: '.payment-conditions',
        payments: '.payments',
        footer: {
            el: 'footer',
            replaceElement: true
        },
    },
    childViewEvents: {
        'status:change': 'onStatusChange',
    },
    initialize: function(options){
        this.channel = Radio.channel('facade');
    },
    showCommonBlock: function(){
        var model = this.channel.request('get:model', 'common');
        var view = new CommonView({model: model});
        this.showChildView('common', view);
    },
    showTaskGroupBlock: function(){
        var collection = this.channel.request('get:collection', 'task_groups');
        var view = new TaskBlockView({collection: collection});
        this.showChildView('tasklines', view);
    },
    showDiscountBlock: function(){
        var collection = this.channel.request('get:collection', 'discounts');
        var model = this.channel.request('get:model', 'common');
        var view = new DiscountBlockView({collection: collection, model: model});
        this.showChildView('discounts', view);
    },
    showNotesBlock: function(){
        var model = this.channel.request('get:model', 'common');
        var view = new NotesBlockView({model: model});
        this.showChildView('notes', view);
    },
    showPaymentConditionsBlock: function(){
        var model = this.channel.request('get:model', 'common');
        var view = new PaymentConditionBlockView({model:model});
        this.showChildView('payment_conditions', view);
    },
    showPaymentBlock: function(){
        var model = this.channel.request('get:model', 'common');
        var collection = this.channel.request('get:paymentcollection');
        var view = new PaymentBlockView({model: model, collection: collection});
        this.showChildView('payments', view);
    },
    showLogin: function(){
        var view = new LoginView({});
        this.showChildView('modalRegion', view);
    },
    onRender: function() {
        if (_.indexOf(AppOption['form_options']['sections'], "common") != -1){
            this.showCommonBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "tasklines") != -1){
            this.showTaskGroupBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "discounts") != -1){
            this.showDiscountBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "notes") != -1){
            this.showNotesBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "payment_conditions") != -1){
            this.showPaymentConditionsBlock();
        }
        if (_.indexOf(AppOption['form_options']['sections'], "payments") != -1){
            this.showPaymentBlock();
        }

        var totalmodel = this.channel.request('get:totalmodel');
        var view = new RightBarView(
            {
                actions: AppOption['form_options']['actions'],
                model: totalmodel
            }
        );
        this.showChildView('rightbar', view);
        view = new BootomActionView(
            {actions: AppOption['form_options']['actions']}
        );
        this.showChildView('footer', view);

        view = new HtBeforeDiscountsView({model: totalmodel});
        this.showChildView('ht_before_discounts', view);
        view = new TotalView({model: totalmodel});
        this.showChildView('totals', view);
    },
    showStatusView(status, title, label, url){
        console.log("Showing the status view");
        this.showChildView(
            'modalRegion',
            new StatusView({
                status: status,
                title: title,
                label: label,
                model: this.commonModel,
                url: url
            })
        );
    },
    onStatusChange: function(status, title, label, url){
        var common_model = this.channel.request('get:model', 'common');
        var this_ = this;
        // We ensure the common_model get saved before changing the status
        common_model.save(
            null,
            {
                patch:true,
                success: function(){
                    this_.showStatusView(status, title, label, url)
                }
            }
        );
    },
    onChildviewDestroyModal: function() {
    	this.getRegion('modalRegion').empty();
  	}
});
export default MainView;
