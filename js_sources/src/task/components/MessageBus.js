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
    },
    logSuccess(view, message){
        console.log("MessageBus : " + message);
    },
    logError(view, message){
        console.error("MessageBus : " + message);
    }
});
const MessageBus = new MessageBusClass();
export default MessageBus;
