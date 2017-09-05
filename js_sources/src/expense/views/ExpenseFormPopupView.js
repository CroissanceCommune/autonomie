/*
 * File Name : ExpenseFormPopupView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import ModalBehavior from '../../base/behaviors/ModalBehavior.js';
import ExpenseFormView from './ExpenseFormView.js';
import Radio from 'backbone.radio';
import BookMarkCollectionView from './BookMarkCollectionView.js';

const ExpenseFormPopupView = Mn.View.extend({
    behaviors: [ModalBehavior],
    template: require('./templates/ExpenseFormPopupView.mustache'),
    regions: {
        main: '#mainform-container',
        tel: '#telform-container',
        bookmark: '#bookmark-container',
    },
    ui: {
        main_tab: 'ul.nav-tabs li.main a',
        tel_tab: "ul.nav-tabs li.tel a",
        modalbody: '.modal-body',
    },
    childViewEvents: {
        'bookmark:insert': 'onBookMarkInsert',
        'success:sync': 'onSuccessSync',
    },
    // Here we bind the child FormBehavior with our ModalBehavior
    // Like it's done in the ModalFormBehavior
    childViewTriggers: {
        'cancel:form': 'modal:close',
        'bookmark:delete': 'bookmark:delete',
    },
    modelEvents: {
        'set:bookmark': 'refreshForm',
    },
    initialize(){
        var facade = Radio.channel('facade');
        this.bookmarks = facade.request('get:bookmarks');
        this.add = this.getOption('add');
        this.tel = this.model.isSpecial();
    },
    refresh(){
        this.triggerMethod('line:add', this.model.get('category'));
    },
    onSuccessSync(){
        if (this.add){
            var this_ = this;
            var modalbody = this.getUI('modalbody');

            modalbody.effect(
                'highlight',
                {color: '#bbdfbb'},
                800,
                this_.refresh.bind(this)
            );
        } else {
            this.triggerMethod('modal:close');
        }
    },
    onModalBeforeClose(){
        this.model.rollback();
    },
    refreshForm(){
        if (this.model.isSpecial()){
            this.showTelForm();
            this.getUI('tel_tab').tab('show');
        } else {
            this.showMainForm();
            this.getUI('main_tab').tab('show');
        }
    },
    showMainForm(){
        if ((!this.tel) || this.add){
            var view = new ExpenseFormView({
                model: this.model,
                destCollection: this.getOption('destCollection'),
                title: this.getOption('title'),
                tel: false,
                add: this.add,
            });
            this.showChildView('main', view);
        }
    },
    showTelForm(){
        if (this.tel || this.add){
            var view = new ExpenseFormView({
                model: this.model,
                destCollection: this.getOption('destCollection'),
                title: this.getOption('title'),
                tel: true,
                add: this.add,
            });
            this.showChildView('tel', view);
        }
    },
    onBookMarkInsert(childView){
        this.model.loadBookMark(childView.model);
    },
    showBookMarks(){
        if (this.add){
            if (this.bookmarks.length > 0){
                var view = new BookMarkCollectionView({
                    collection: this.bookmarks
                });
                this.showChildView('bookmark', view);
            }
        }
    },
    templateContext(){
        /*
         * Form can be add form : show all tabs
         * Form can be tel form : show only the tel tab
         */
        var show_tel = this.add || this.tel;
        var show_main = this.add || ! this.tel;
        return {
            title: this.getOption('title'),
            add: this.add,
            show_tel: show_tel,
            show_bookmarks: this.add && this.bookmarks.length > 0,
            show_main: show_main,
        }
    },
    onRender: function(){
        this.refreshForm();
        this.showTelForm();
        this.showBookMarks();
    },
});
export default ExpenseFormPopupView;
