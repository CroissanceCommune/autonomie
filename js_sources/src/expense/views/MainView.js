/*
 * File Name : MainView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Radio from 'backbone.radio';

import RightBarView from "./RightBarView.js";
import StatusView from './StatusView.js';
import BootomActionView from './BootomActionView.js';
import ExpenseModel from '../models/ExpenseModel.js';
import ExpenseKmModel from '../models/ExpenseKmModel.js';
import ExpenseTableView from './ExpenseTableView.js';
import ExpenseKmTableView from './ExpenseKmTableView.js';
import ExpenseFormPopupView from './ExpenseFormPopupView.js';
import ExpenseKmFormView from './ExpenseKmFormView.js';
import ExpenseDuplicateFormView from './ExpenseDuplicateFormView.js';
import TotalView from './TotalView.js';
import TabTotalView from './TabTotalView.js';
import {displayServerSuccess, displayServerError} from '../../backbone-tools.js';

const MainView = Mn.View.extend({
    className: 'container-fluid page-content',
   template: require('./templates/MainView.mustache'),
   regions: {
       modalRegion: '.modalRegion',
       internalLines: '.internal-lines',
       internalKmLines: '.internal-kmlines',
       internalTotal: '.internal-total',
       activityLines: '.activity-lines',
       activityKmLines: '.activity-kmlines',
       activityTotal: '.activity-total',
       totals: '.totals',
       footer: {
           el: '.footer-actions',
           replaceElement: true
       },
       rightbar: "#rightbar",
   },
   ui:{
       internal: '#internal-container',
       activity: '#activity-container',
   },
   childViewEvents: {
       'line:add': 'onLineAdd',
       'line:edit': 'onLineEdit',
       'line:delete': 'onLineDelete',
       'kmline:add': 'onKmLineAdd',
       'kmline:edit': 'onKmLineEdit',
       'kmline:delete': 'onLineDelete',
       'line:duplicate': 'onLineDuplicate',
       'kmline:duplicate': 'onLineDuplicate',
       'bookmark:add': 'onBookMarkAdd',
       'bookmark:delete': 'onBookMarkDelete',
       "status:change": 'onStatusChange',
   },
   initialize(){
       this.facade = Radio.channel('facade');
       this.config = Radio.channel('config');
       this.categories = this.config.request('get:options', 'categories');
       this.edit = this.config.request('get:options', 'edit');
   },
   onLineAdd(childView){
       /*
        * Launch when a line should be added
        *
        * :param childView: category 1/2 or a childView with a category option
        */
       var category;
       if (_.isNumber(childView) || _.isString(childView)){
           category = childView;
       }else{
           category = childView.getOption('category').value;
       }
       var model = new ExpenseModel({category: category});
       this.showLineForm(model, true, "Enregistrer une dépense");
   },
   onKmLineAdd(childView){
       var category = childView.getOption('category').value;
       var model = new ExpenseKmModel({category: category});
       this.showKmLineForm(model, true, "Enregistrer une dépense");
   },
   onLineEdit(childView){
       this.showLineForm(childView.model, false, "Modifier une dépense");
   },
   onKmLineEdit(childView){
       this.showKmLineForm(childView.model, false, "Modifier une dépense");
   },
   showLineForm(model, add, title){
       var view = new ExpenseFormPopupView({
           title: title,
           add:add,
           model:model,
           destCollection: this.facade.request('get:collection', 'lines'),
       });
       this.showChildView('modalRegion', view);
   },
   showKmLineForm(model, add, title){
       var view = new ExpenseKmFormView({
           title: title,
           add:add,
           model:model,
           destCollection: this.facade.request('get:collection', 'kmlines'),
       });
       this.showChildView('modalRegion', view);
   },
   showDuplicateForm(model){
       var view = new ExpenseDuplicateFormView({model: model});
       this.showChildView('modalRegion', view);
   },
   onLineDuplicate(childView){
       this.showDuplicateForm(childView.model);
   },
   onDeleteSuccess: function(){
       displayServerSuccess("Vos données ont bien été supprimées");
   },
   onDeleteError: function(){
       displayServerError("Une erreur a été rencontrée lors de la " +
                           "suppression de cet élément");
   },
   onLineDelete: function(childView){
       var result = window.confirm("Êtes-vous sûr de vouloir supprimer cette dépense ?");
       if (result){
           childView.model.destroy(
               {
                   success: this.onDeleteSuccess,
                   error: this.onDeleteError
               }
           );
       }
    },
   onBookMarkAdd(childView){
       var collection = this.facade.request('get:bookmarks');
       collection.addBookMark(childView.model);
       childView.highlightBookMark();
   },
   onBookMarkDelete(childView){
       var result = window.confirm("Êtes-vous sûr de vouloir supprimer ce favoris ?");
       if (result){
           childView.model.destroy(
               {
                   success: this.onDeleteSuccess,
                   error: this.onDeleteError
               }
           );
       }
   },
   showInternalTab(){
       var collection = this.facade.request(
           'get:collection',
           'lines'
       );
       var view = new ExpenseTableView({
           collection: collection,
           category: this.categories[0],
           edit: this.edit,
       });
       this.showChildView('internalLines', view);

       var km_type_options = this.config.request(
            'get:options',
            'expensekm_types',
       );
       if (km_type_options.length !== 0){
           collection = this.facade.request(
               'get:collection',
               'kmlines'
           );
           view = new ExpenseKmTableView(
               {
                   collection: collection,
                   category: this.categories[0],
                   edit: this.edit,
               }
           );
           this.showChildView('internalKmLines', view);
       }
   },
   showActitityTab(){
       var collection = this.facade.request(
           'get:collection',
           'lines'
       );
       var view = new ExpenseTableView(
           {
               collection: collection,
               category: this.categories[1],
               edit: this.edit,
           }
       );
       this.showChildView('activityLines', view);

       var km_type_options = this.config.request(
            'get:options',
            'expensekm_types',
       );
       if (km_type_options.length !== 0){
           collection = this.facade.request(
               'get:collection',
               'kmlines'
           );
           view = new ExpenseKmTableView(
               {
                   collection: collection,
                   category: this.categories[1],
                   edit: this.edit,
               }
           );
           this.showChildView('activityKmLines', view);
       }
   },
   showActions(){
       var view = new RightBarView(
           {
               actions: this.config.request('get:form_actions'),
           }
       );
       this.showChildView('rightbar', view);

       view = new BootomActionView(
           {
               actions: this.config.request('get:form_actions')
           }
       );
       this.showChildView('footer', view);
   },
   showTotals(){
       let model = this.facade.request('get:totalmodel');
       var view = new TotalView({model: model});
       this.showChildView('totals', view);

       view = new TabTotalView({model: model, category: 1});
       this.showChildView('internalTotal', view);
       view = new TabTotalView({model: model, category: 2});
       this.showChildView('activityTotal', view);
   },
   onRender(){
       this.showInternalTab();
       this.showActitityTab();
       this.showTotals();
       this.showActions();
   },
   onStatusChange(status, title, label, url){
       var view = new StatusView({
           status: status,
           title: title,
           label: label,
           url: url
       });
       this.showChildView('modalRegion', view);
   },
});
export default MainView;
