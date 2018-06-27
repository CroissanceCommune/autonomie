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

import FileBlockView from "./FileBlockView.js";
import GeneralView from "./GeneralView.js";
import CommonView from "./CommonView.js";
import TaskBlockView from './TaskBlockView.js';
import HtBeforeDiscountsView from './HtBeforeDiscountsView.js';
import DiscountBlockView from './DiscountBlockView.js';
import ExpenseHtBlockView from './ExpenseHtBlockView.js';
import TotalView from './TotalView.js';
import NotesBlockView from './NotesBlockView.js';
import PaymentConditionBlockView from './PaymentConditionBlockView.js';
import PaymentBlockView from './PaymentBlockView.js';

import RightBarView from "./RightBarView.js";
import StatusView from './StatusView.js';
import BootomActionView from './BootomActionView.js';
import LoginView from '../../base/views/LoginView.js';
import ErrorView from './ErrorView.js';
import { showLoader, hideLoader } from '../../tools.js';

const template = require('./templates/MainView.mustache');

const MainView = Mn.View.extend({
    template: template,
    regions: {
        errors: '.errors',
        modalRegion: '#modalregion',
        file_requirements: "#file_requirements",
        general: '#general',
        common: '#common',
        tasklines: '#tasklines',
        discounts: '#discounts',
        expenses_ht: '#expenses_ht',
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
        this.config = Radio.channel('config');
        this.facade = Radio.channel('facade');
    },
    showFileBlock: function(){
        var section = this.config.request(
            'get:form_section', 'file_requirements'
        );
        var collection = this.facade.request(
            'get:collection', 'file_requirements'
        );
        var view = new FileBlockView(
            {collection: collection, section:section}
        );
        this.showChildView('file_requirements', view);
    },
    showGeneralBlock: function(){
        var section = this.config.request('get:form_section', 'general');
        var model = this.facade.request('get:model', 'common');
        var view = new GeneralView({model: model, section: section});
        this.showChildView('general', view);
    },
    showCommonBlock: function(){
        var section = this.config.request('get:form_section', 'common');
        var model = this.facade.request('get:model', 'common');
        var view = new CommonView({model: model, section: section});
        this.showChildView('common', view);
    },
    showTaskGroupBlock: function(){
        var section = this.config.request('get:form_section', 'tasklines');
        var model = this.facade.request('get:model', 'common');
        var collection = this.facade.request(
            'get:collection',
            'task_groups'
        );
        var view = new TaskBlockView(
            {collection: collection, section:section, model:model}
        );
        this.showChildView('tasklines', view);
    },
    showDiscountBlock: function(){
        var section = this.config.request('get:form_section', 'discounts');
        var collection = this.facade.request(
            'get:collection',
            'discounts'
        );
        var model = this.facade.request('get:model', 'common');
        var view = new DiscountBlockView(
            {collection: collection, model: model, section: section}
        );
        this.showChildView('discounts', view);
    },
    showExpenseHtBlock: function(){
        var section = this.config.request('get:form_section', 'expenses_ht');
        var model = this.facade.request('get:model', 'common');
        var view = new ExpenseHtBlockView({model: model, section: section});
        this.showChildView('expenses_ht', view);
    },
    showNotesBlock: function(){
        var section = this.config.request('get:form_section', 'notes');
        var model = this.facade.request('get:model', 'common');
        var view = new NotesBlockView({model: model, section: section});
        this.showChildView('notes', view);
    },
    showPaymentConditionsBlock: function(){
        var section = this.config.request('get:form_section', 'payment_conditions');
        var model = this.facade.request('get:model', 'common');
        var view = new PaymentConditionBlockView({model:model});
        this.showChildView('payment_conditions', view);
    },
    showPaymentBlock: function(){
        var section = this.config.request('get:form_section', 'payments');
        var model = this.facade.request('get:model', 'common');
        var collection = this.facade.request('get:paymentcollection');
        var view = new PaymentBlockView(
            {model: model, collection: collection, section: section}
        );
        this.showChildView('payments', view);
    },
    showLogin: function(){
        var view = new LoginView({});
        this.showChildView('modalRegion', view);
    },
    onRender: function() {
        var totalmodel = this.facade.request('get:totalmodel');
        var view;
        if (this.config.request('has:form_section', 'file_requirements')){
            this.showFileBlock();
        }
        if (this.config.request('has:form_section', 'general')){
            this.showGeneralBlock();
        }
        if (this.config.request('has:form_section', 'common')){
            this.showCommonBlock();
        }
        if (this.config.request('has:form_section', "tasklines")){
            this.showTaskGroupBlock();
        }
        if (this.config.request('has:form_section', "discounts")){
            view = new HtBeforeDiscountsView({model: totalmodel});
            this.showChildView('ht_before_discounts', view);
            this.showDiscountBlock();
        }
        if (this.config.request('has:form_section', "expenses_ht")){
            this.showExpenseHtBlock();
        }

        view = new TotalView({model: totalmodel});
        this.showChildView('totals', view);

        if (this.config.request('has:form_section', "notes")){
            this.showNotesBlock();
        }
        if (this.config.request('has:form_section', "payment_conditions")){
            this.showPaymentConditionsBlock();
        }
        if (this.config.request('has:form_section', "payments")){
            this.showPaymentBlock();
        }

        view = new RightBarView(
            {
                actions: this.config.request('get:form_actions'),
                model: totalmodel
            }
        );
        this.showChildView('rightbar', view);
        view = new BootomActionView(
            {actions: this.config.request('get:form_actions')}
        );
        this.showChildView('footer', view);
    },
    showStatusView(status, title, label, url){
        var model = this.facade.request('get:model', 'common');
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
        var errors = this.facade.request('is:valid');
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
                document.body.scrollTop = document.documentElement.scrollTop = 0;
                hideLoader();
                return;
            }
        }
        hideLoader();
        var common_model = this.facade.request('get:model', 'common');
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
