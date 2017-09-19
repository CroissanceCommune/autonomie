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
import BaseFormBehavior from './BaseFormBehavior.js';
import Radio from 'backbone.radio';

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
    onSyncError(datas, status, result){
        var channel = Radio.channel("message");
        channel.trigger('error:backbone', result);
        Validation.unbind(this.view);
    },
    onSyncSuccess(datas, status, result){
        var channel = Radio.channel("message");
        channel.trigger('success:backbone', result);
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

        if (this.view.model.isValid(_.keys(datas))){
            let request;
            if (! this.view.model.get('id')){
                request = this.addSubmit(datas);
            } else {
                request = this.editSubmit(datas);
            }
            console.log(request);
            request.done(this.onSyncSuccess.bind(this)
                        ).fail(this.onSyncError.bind(this)
                              );
        }
    },
    addSubmit(datas){
        /*
         *
         * Since collection.create doesn't return a jquery promise, we need to
         * re-implement the destcollection create stuff and return the expected
         * promise
         *
         * See sources : (Collection.create)
         * http://backbonejs.org/docs/backbone.html
         *
         */
        console.log("FormBehavior.addSubmit");
        var destCollection = this.view.getOption('destCollection');
        let model = destCollection._prepareModel(datas);

        var request = model.save(
            null,
            {wait: true, sort: true}
        );
        request = request.done(
            function(model, resp, callbackOpts){
                destCollection.add(model, callbackOpts);
                return model, 'success', resp;
            }
        );
        return request;
    },
    editSubmit(datas){
        console.log("FormBehavior.editSubmit");
        return this.view.model.save(datas, {wait: true, patch:true});
    },
    onSubmitForm(event){
        console.log("FormBehavior.onSubmitForm");
        event.preventDefault();
        var datas = this.serializeForm();
        this.view.model.set(datas, {validate: true});
        this.syncServer(datas);
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
