/*
 * File Name : MessageView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Bb from 'backbone';
import Radio from 'backbone.radio';

const MessageView = Mn.View.extend({
    tagName: 'div',
    template: require('./templates/MessageView.mustache'),
    ui: {
        close: 'span.link'
    },
    events: {
        'click @ui.close': 'onClose',
    },
    modelEvents: {
        "change:notifyClass": 'render',
    },
    className: 'messages-static-top text-center alert',
    onClose(){
        this.model.set({notifyText: null});
        this.$el.hide();
    },
    initialize() {
        const channel = Radio.channel('message');
        channel.reply({
            'notify:success': this.notifySuccess.bind(this),
            'notify:error': this.notifyError.bind(this)
        });
    },
    notifyError(message) {
        console.log("Notify error");
        this.model.set({
    	    notifyClass: 'error',
  	        notifyText: message
    	});
        this.$el.removeClass('alert-success');
        this.$el.addClass('alert-danger');
        this.$el.show();
    },
    notifySuccess(message) {
        console.log("Notify success");
        this.model.set({
            notifyClass: 'success',
            notifyText: message
        });
        this.$el.removeClass('alert-danger');
        this.$el.addClass('alert-success');
        this.$el.show();
    },
    templateContext(){
        var has_message = false;
        if (this.model.get('notifyText')){
            has_message = true;
        }
        return {
            has_message: has_message,
            error: this.model.get('notifyClass') == 'error'
        }
    }
});
export default MessageView;
