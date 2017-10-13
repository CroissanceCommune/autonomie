/*
 * File Name : DiscountCollectionView.js
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
import DiscountView from './DiscountView.js';
import Validation from 'backbone-validation';

const DiscountCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    className: 'col-xs-12',
    childView: DiscountView,
    // Bubble up child view events
    childViewTriggers: {
        'edit': 'line:edit',
        'delete': 'line:delete'
    },
    initialize: function(options){
        var channel = Radio.channel('facade');
        this.listenTo(channel, 'bind:validation', this.bindValidation);
        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
        this.listenTo(this.model, 'validated:invalid', this.showErrors);
        this.listenTo(this.model, 'validated:valid', this.hideErrors.bind(this));
    },
    showErrors(model, errors){
        this.$el.addClass('error');
    },
    hideErrors(model){
        this.$el.removeClass('error');
    },
    bindValidation(){
        Validation.bind(this);
    },
    unbindValidation(){
        Validation.unbind(this);
    },
});
export default DiscountCollectionView;
