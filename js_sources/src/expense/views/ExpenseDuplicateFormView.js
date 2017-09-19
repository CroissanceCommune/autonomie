/*
 * File Name : ExpenseDuplicateFormView.js
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
import ModalBehavior from '../../base/behaviors/ModalBehavior.js';
import SelectWidget from '../../widgets/SelectWidget.js';
import { serializeForm } from '../../tools.js';
import { formatAmount } from '../../math.js';

const ExpenseDuplicateFormView = Mn.View.extend({
    behaviors: [ModalBehavior],
    template: require('./templates/ExpenseDuplicateFormView.mustache'),
    regions: {
        'select': '.select'
    },
    ui: {
        cancel_btn: 'button[type=reset]',
        form: 'form',
    },
    events: {
        'submit @ui.form': 'onSubmit',
        'click @ui.cancel_btn': 'onCancelClick',
    },
    initialize(){
        var channel = Radio.channel('config');
        this.options = channel.request('get:options', 'expenses');
    },
    onCancelClick(){
        this.triggerMethod('modal:close');
    },
    templateContext(){
        var ht = this.model.getHT();
        var tva = this.model.getTva();
        var ttc = this.model.total();
        var is_km_fee = this.model.get('type') == 'km'
        return {
            ht: formatAmount(ht),
            tva: formatAmount(tva),
            ttc: formatAmount(ttc),
            is_km_fee: is_km_fee
        }
    },
    onRender(){
        var view = new SelectWidget({
            options: this.options,
            title: 'Feuille de note de dépenses vers laquelle dupliquer',
            id_key: 'id',
            field_name: 'sheet_id',
        });
        this.showChildView('select', view);
    },
    onSubmit(event){
        event.preventDefault();
        var datas = serializeForm(this.getUI('form'));
        var request = this.model.duplicate(datas);
        var this_ = this;
        request.done(function(){
            this_.triggerMethod('modal:close')
        });
    },
});
export default ExpenseDuplicateFormView;
