/*
 * File Name : ModalFormBehavior.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Validation from 'backbone-validation';
import { serializeForm } from '../../tools.js';
import {BootstrapOnInvalidForm, BootstrapOnValidForm, displayServerError, displayServerSuccess} from '../../backbone-tools.js';
import ModalBehavior from './ModalBehavior.js';

var ModalFormBehavior = Mn.Behavior.extend({
    behaviors: [ModalBehavior],
	ui: {
        form: "form",
        submit: "button[type=submit]"
    },
    events: {
        'click @ui.submit': 'onSubmitForm',
        'submit @ui.form': 'onSubmitForm'
    },
    defaults: {
        errorMessage: "Une erreur est survenue"
    },
    serializeForm: function(){
        return serializeForm(this.getUI('form'));
    },
    onSyncError: function(){
        displayServerError("Une erreur a été rencontrée lors de la " +
                           "sauvegarde de vos données");
        Validation.unbind(this.view);
    },
    onSyncSuccess: function(){
        displayServerSuccess("Vos données ont bien été sauvegardées");
        Validation.unbind(this.view);
        this.view.triggerMethod('modal:close');
    },
    syncServer: function(datas, bound){
        var bound = bound || false;
        var datas = datas || this.view.model.toJSON();

        if (!bound){
            Validation.bind(this.view, {
                attributes: function(view){return _.keys(datas)}
            });
        }
        if (this.view.model.isValid()){
            if (! this.view.model.get('id')){
                this.addSubmit(datas);
            } else {
                this.editSubmit(datas);
            }
        }
    },
    addSubmit: function(datas){
        var destCollection = this.view.getOption('destCollection');
        destCollection.create(
            datas,
            {
                success: this.onSyncSuccess.bind(this),
                error: this.onSyncError.bind(this),
                wait: true,
                sort: true
            },
        )
    },
    editSubmit: function(datas){
        this.view.model.save(
            datas,
            {
                success: this.onSyncSuccess.bind(this),
                error: this.onSyncError.bind(this),
                wait: true
            }
        );
    },
    onSubmitForm: function(event){
        event.preventDefault();
        this.view.model.set(this.serializeForm(), {validate: true});
        this.syncServer();
    },
    onDataPersist: function(view, attribute, value){
        Validation.unbind(this.view);
        Validation.bind(this.view, {
            attributes: function(view){return [attribute];}
        });

        var datas = {};
        datas[attribute] = value;
        this.view.model.set(datas);
        this.syncServer(datas, true);
    },
    onDataModified: function(view, attribute, value){
        Validation.unbind(this.view);
        Validation.bind(this.view, {
            attributes: function(view){return [attribute];}
        });
        var datas = {};
        datas[attribute] = value;
        this.view.model.set(datas);
        this.view.model.isValid();
    }
});

export default ModalFormBehavior;
