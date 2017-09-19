/*
 * File Name : MessageBus.js
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


const MessageBusClass = Mn.Object.extend({
    channelName: 'message',
    radioEvents: {
        'success': 'logSuccess',
        'error': 'logError',
        'error:ajax': 'onAjaxError',
        'success:ajax': 'onAjaxSuccess',
        'error:backbone': 'onAjaxError',
        'success:backbone': 'onAjaxSuccess',
    },
    logSuccess(view, message){
        console.log("MessageBus : " + message);
        this.getChannel().request('notify:success', message);
    },
    logError(view, message){
        console.error("MessageBus : " + message);
        this.getChannel().request('notify:error', message);
    },
    extractJsonMessage(xhr){
        let json_resp = xhr.responseJSON;
        let result = null;
        if (!_.isUndefined(json_resp)){
            if (!_.isUndefined(json_resp.message)){
                result = json_resp.message;
            }else if (!_.isUndefined(json_resp.messages)){
                result = json_resp.messages.join("<br />");
            } else if (!_.isUndefined(json_resp.errors)){
                result = json_resp.errors.join("<br />");
            } else if (!_.isUndefined(json_resp.error)){
                result =  json_resp.error;
            } else if (json_resp.status == 'success'){
                result = "Opération réussie";
            } else if (xhr.status == 200){
                result = "Opération réussie";
            }
        } else if (xhr.status == 403){
            result = "Opération non permise";
        } else if (xhr.status == 501){
            result = "Une erreur inconnue est survenue, contactez votre administrateur";
        }
        return result
    },
    onAjaxError(xhr){
        let message = this.extractJsonMessage(xhr);
        if (!_.isNull(message)){
            this.getChannel().request('notify:error', message);
        }
    },
    onAjaxSuccess(xhr){
        let message = this.extractJsonMessage(xhr);
        if (!_.isNull(message)){
            this.getChannel().request('notify:success', message);
        }
    }
});
const MessageBus = new MessageBusClass();
export default MessageBus;
