/*
 * File Name : AuthBus.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { ajax_call } from '../../tools.js';

const AuthBusClass = Mn.Object.extend({
    channelName: 'auth',
    url: '/api/v1/login',
    radioEvents: {
        'login': 'onLogin',
    },
    initialize: function(){
        this.ok_callback = null;
        this.error_callback = null;
    },
    setAuthCallbacks(callbacks){
        /*
         * Define authentication callbacks that should be fired
         * on successfull authentication
         */
        this.callbacks = callbacks;
    },
    onLogin(datas, onAuthOk, onAuthFailed){
        var callbacks = this.callbacks;
        this.ok_callback = onAuthOk;
        this.error_callback = onAuthFailed;
        ajax_call(
            this.url,
            datas,
            'POST',
            {
                success: this.onAuthSuccess.bind(this),
                error: this.onAuthError.bind(this)
            }
        );
    },
    onAuthSuccess(result){
        if (result['status'] == 'success'){
            _.each(this.callbacks, function(callback){
                callback();
            });
            this.ok_callback(result);
        } else {
            this.error_callback(result);
        }
    },
    onAuthError(xhr){
        if (xhr.status == 400){
               if (_.has(xhr.responseJSON, 'errors')){
                   this.error_callback(xhr.responseJSON.errors);
               } else {
                   this.error_callback();
               }
        } else {
            alert('Erreur serveur : contactez votre administrateur');
        }
    }
});
const AuthBus = new AuthBusClass;
export default AuthBus;
