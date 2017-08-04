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

import StatusHistoryView from './StatusHistoryView.js';
import GeneralView from "./GeneralView.js";
import CommonView from "./CommonView.js";
import TaskBlockView from './TaskBlockView.js';
import HtBeforeDiscountsView from './HtBeforeDiscountsView.js';
import DiscountBlockView from './DiscountBlockView.js';
import TotalView from './TotalView.js';
import NotesBlockView from './NotesBlockView.js';
import PaymentConditionBlockView from './PaymentConditionBlockView.js';
import PaymentBlockView from './PaymentBlockView.js';

import RightBarView from "./RightBarView.js";
import StatusView from './StatusView.js';
import BootomActionView from './BootomActionView.js';
import LoginView from './LoginView.js';
import ErrorView from './ErrorView.js';
import { showLoader, hideLoader } from '../../tools.js';

const template = require('./templates/MainView.mustache');

const MainView = Mn.View.extend({
    template: template,
    regions: {
        errors: '.errors',
        status_history: '.status_history',
        modalRegion: '#modalregion',
        general: '#general',
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
            el: '.footer-actions',
            replaceElement: true
        },
    },
    childViewEvents: {
        'status:change': 'onStatusChange',
    },
    initialize: function(options){
        this.channel = Radio.channel('facade');
    },
    showStatusHistory(){
        var collection = Radio.channel('facade').request(
            'get:status_history_collection'
        );
        if (collection.models.length > 0){
            var view = new StatusHistoryView({collection: collection});
            this.showChildView('status_history', view);
        }
    },
    showGeneralBlock: function(){
        var model = this.channel.request('get:model', 'common');
        var view = new GeneralView({model: model});
        this.showChildView('general', view);
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
        this.showStatusHistory();
        var totalmodel = this.channel.request('get:totalmodel');
        var view;

        if (this.channel.request('has:form_section', 'general')){
            this.showGeneralBlock();
        }
        if (this.channel.request('has:form_section', 'common')){
            this.showCommonBlock();
        }
        if (this.channel.request('has:form_section', "tasklines")){
            this.showTaskGroupBlock();
        }
        if (this.channel.request('has:form_section', "discounts")){
            view = new HtBeforeDiscountsView({model: totalmodel});
            this.showChildView('ht_before_discounts', view);
            this.showDiscountBlock();
        }

        view = new TotalView({model: totalmodel});
        this.showChildView('totals', view);

        if (this.channel.request('has:form_section', "notes")){
            this.showNotesBlock();
        }
        if (this.channel.request('has:form_section', "payment_conditions")){
            this.showPaymentConditionsBlock();
        }
        if (this.channel.request('has:form_section', "payments")){
            this.showPaymentBlock();
        }

        view = new RightBarView(
            {
                actions: this.channel.request('get:form_actions'),
                model: totalmodel
            }
        );
        this.showChildView('rightbar', view);
        view = new BootomActionView(
            {actions: this.channel.request('get:form_actions')}
        );
        this.showChildView('footer', view);
    },
    showStatusView(status, title, label, url){
        var model = this.channel.request('get:model', 'common');
        var view = new StatusView({
            status: status,
            title: title,
            label: label,
            model: model,
            url: url
        });
        this.showChildView('modalRegion', view);
    },
    formOk(){
        var result = true;
        var errors = this.channel.request('is:valid');
        if (!_.isEmpty(errors)){
            this.showChildView(
                'errors',
                new ErrorView({errors:errors})
            );
            result = false;
        } else {
            this.detachChildView('errors');
        }
        return result;

    },
    onStatusChange: function(status, title, label, url){
        showLoader();
        if (status != 'draft'){
            if (! this.formOk()){
                hideLoader();
                return;
            }
        }
        hideLoader();
        var common_model = this.channel.request('get:model', 'common');
        var this_ = this;
        // We ensure the common_model get saved before changing the status
        common_model.save(
            null,
            {
                patch:true,
                success: function(){
                    this_.showStatusView(status, title, label, url)
                },
                error: function(){
                    hideLoader();
                }
            }
        );
    },
    onChildviewDestroyModal: function() {
    	this.getRegion('modalRegion').empty();
  	}
});
export default MainView;
