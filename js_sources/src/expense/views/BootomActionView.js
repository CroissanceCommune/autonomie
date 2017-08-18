/*
 * File Name : BootomActionView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';

const BootomActionView = Mn.View.extend({
    template: require('./templates/BootomActionView.mustache'),
    tagName: 'footer',
    className: 'sticky-footer hidden-md hidden-lg text-center',
    ui: {
        buttons: 'button',
    },
    events: {
        'click @ui.buttons': 'onButtonClick'
    },
    templateContext: function(){
        return {
            buttons: this.getOption('actions')['status'],
        }
    },
    onButtonClick: function(event){
        let target = $(event.target);
        let status = target.data('status');
        let title = target.data('title');
        let label = target.data('label');
        let url = target.data('url');
        this.triggerMethod('status:change', status, title, label, url);
    },

});
export default BootomActionView;
