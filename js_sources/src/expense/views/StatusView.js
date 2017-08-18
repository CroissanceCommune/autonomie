/*
 * File Name : StatusView.js
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
import { serializeForm, ajax_call, showLoader, hideLoader } from '../../tools.js';
import Radio from 'backbone.radio';
import { parseDate, dateToIso } from '../../date.js';

var template = require("./templates/StatusView.mustache");

const StatusView = Mn.View.extend({
    template: template,
    ui: {
        'textarea': 'textarea',
        btn_cancel: '.cancel',
        submit: 'button[type=submit]',
        form: 'form'
    },
    behaviors: {
        modal: {
            behaviorClass: ModalBehavior
        }
    },
    events: {
        'click @ui.btn_cancel': 'destroy',
        'click @ui.submit': 'onSubmit'
    },
    submitCallback: function(result){
    },
    submitErroCallback: function(result){
        hideLoader();
        var message = ""
        if (result.responseJSON.errors){
            _.each(result.responseJSON.errors, function(error, key){
                message += "   " + key + ":" + error
            });
        }
        if (message == ''){
            message = "Votre document est incomplet, merci de vérifier votre saisie."
        }
        window.alert(message);
    },
    onSubmit: function(event){
        event.preventDefault();
        let datas = serializeForm(this.getUI('form'));
        datas['submit'] = this.getOption('status');
        const url = this.getOption('url');
        showLoader();
        this.serverRequest = ajax_call(url, datas, "POST");
        this.serverRequest.then(
            this.submitCallback.bind(this), this.submitErroCallback.bind(this)
        );
    },
    templateContext: function(){
        let result = {
            title: this.getOption('title'),
            label: this.getOption('label'),
            status: this.getOption('status'),
            url: this.getOption('url'),
        }
        return result;
    }
});
export default StatusView;
