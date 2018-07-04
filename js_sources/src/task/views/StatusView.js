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
import { FileRequirementCollectionView } from './FileBlockView.js';

var template = require("./templates/StatusView.mustache");

const StatusView = Mn.View.extend({
    template: template,
    ui: {
        'textarea': 'textarea',
        btn_cancel: '.cancel',
        submit: 'button[type=submit]',
        form: 'form',
        force_file_validation: "input[name=force_file_validation]",
    },
    regions: {
        files: ".files",
    },
    behaviors: {
        modal: {
            behaviorClass: ModalBehavior
        }
    },
    events: {
        'click @ui.force_file_validation': "onForceFileValidationClick",
        'click @ui.btn_cancel': 'destroy',
        'click @ui.submit': 'onSubmit'
    },
    initialize: function(options){
        this.facade = Radio.channel('facade');
    },
    submitCallback(result){
    },
    submitErroCallback(result){
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
    onForceFileValidationClick(event){
        const checked = this.ui.force_file_validation.is(':checked');
        this.ui.submit.attr("disabled", !checked);
    },
    onSubmit(event){
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
    fileWarning(){
        const validation_status = this.getOption('status');
        let has_warning;
        if (validation_status != "invalid"){
            has_warning = this.facade.request('has:filewarning', validation_status);
        }else{
            has_warning = false;
        }
        return has_warning
    },
    dateWarning(){
        const validation_status = this.getOption('status');
        var result = {};
        console.log("validation_status : %s", validation_status);
        if (validation_status == 'valid'){
            let model = this.getOption('model');
            let date = model.get('date');
            let today = new Date();
            if ((date != dateToIso(today))){
                result['ask_for_date'] = true;
                date = parseDate(date);
                result['date'] = date.toLocaleDateString();
                result['today'] = today.toLocaleDateString();
                result['has_error'] = true;
            }
        }
        return result;
    },
    templateContext(){
        let result = {
            title: this.getOption('title'),
            label: this.getOption('label'),
            status: this.getOption('status'),
            url: this.getOption('url'),
            ask_for_date: false,
            has_file_warning: this.fileWarning(),
            has_error: this.fileWarning(),
        }
        _.extend(result, this.dateWarning());
        return result;
    },
    onRender(){
        if (this.fileWarning()){
            const collection = this.facade.request('get:filerequirementcollection');
            const view = new FileRequirementCollectionView(
                {collection: collection}
            );
            this.showChildView('files', view);
        }
    }
});
export default StatusView;
