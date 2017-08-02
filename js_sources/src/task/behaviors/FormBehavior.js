/*
 * File Name : FormBehavior.js
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
import {displayServerError, displayServerSuccess} from '../../backbone-tools.js';
import BaseFormBehavior from './BaseFormBehavior.js';

var FormBehavior = Mn.Behavior.extend({
    behaviors: [BaseFormBehavior],
	ui: {
        form: "form",
        submit: "button[type=submit]",
        reset: "button[type=reset]"
    },
    events: {
        'submit @ui.form': 'onSubmitForm',
        'click @ui.reset': 'onCancelClick',
    },
    defaults: {
        errorMessage: "Une erreur est survenue"
    },
    serializeForm(){
        return serializeForm(this.getUI('form'));
    },
    onSyncError(){
        displayServerError("Une erreur a été rencontrée lors de la " +
                           "sauvegarde de vos données");
        Validation.unbind(this.view);
    },
    onSyncSuccess(){
        displayServerSuccess("Vos données ont bien été sauvegardées");
        Validation.unbind(this.view);
        console.log("Trigger success:sync from FormBehavior");
        this.view.triggerMethod('success:sync');
    },
    syncServer(datas, bound){
        var bound = bound || false;
        var datas = datas || this.view.model.toJSON();

        if (!bound){
            Validation.bind(this.view, {
                attributes(view){return _.keys(datas)}
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
    addSubmit(datas){
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
    editSubmit(datas){
        this.view.model.save(
            datas,
            {
                success: this.onSyncSuccess.bind(this),
                error: this.onSyncError.bind(this),
                wait: true
            }
        );
    },
    onSubmitForm(event){
        event.preventDefault();
        this.view.model.set(this.serializeForm(), {validate: true});
        this.syncServer();
    },
    onDataPersisted(datas){
        console.log("FormBehavior.onDataPersisted");
        this.syncServer(datas, true);
    },
    onCancelClick(){
        console.log("FormBehavior.onCancelClick");
        console.log("Trigger reset:model from FormBehavior");
        this.view.triggerMethod('reset:model');
        console.log("Trigger cancel:form from FormBehavior");
        this.view.triggerMethod('cancel:form');
    },
    onResetModel(){
        console.log("FormBehavior.onResetModel");
        this.view.model.rollback();
    },
});

export default FormBehavior;
