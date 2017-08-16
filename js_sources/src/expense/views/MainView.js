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
import ExpenseTableView from './ExpenseTableView.js';
import ExpenseKmTableView from './ExpenseKmTableView.js';

const MainView = Mn.View.extend({
   template: require('./templates/MainView.mustache'),
   regions: {
       modalRegion: '#modalregion',
       internalLines: '.internal-lines',
       internalKmLines: '.internal-kmlines',
       activityLines: '.activity-lines',
       activityKmLines: '.activity-kmlines',
       totals: '.totals',
   },
   ui:{
       internal: '#internal-container',
       activity: '#activity-container',
   },
   initialize(){
       this.facade = Radio.channel('facade');
       this.config = Radio.channel('config');
       this.categories = this.config.requests('get:option', 'categories')
   },
   showInternalTab(){
       var collection = this.facade.requests(
           'get:collection',
           'internal_lines'
       );
       var view = new ExpenseTableView({
           collection: collection,
           category: this.categories[0],
       });
       this.showChildView('internalLines', view);

       collection = this.facade.requests(
           'get:collection',
           'internal_kmlines'
       );
       view = new ExpenseKmTableView(
           {
               collection: collection,
               category: this.categories[0],
           }
       );
       this.showChildView('internalKmLines', view);
   },
   showActitityTab(){
       var collection = this.facade.requests(
           'get:collection',
           'activity_lines'
       );
       var view = new ExpenseTableView(
           {
               collection: collection,
               category: this.categories[1],
           }
       );
       this.showChildView('activityLines', view);

       collection = this.facade.requests(
           'get:collection',
           'activity_kmlines'
       );
       view = new ExpenseKmTableView(
           {
               collection: collection,
               category: this.categories[1],
           }
       );
       this.showChildView('activityKmLines', view);
   },
   onRender(){
       this.showInternalTab();
       this.showActitityTab();
   }
});
export default MainView;
