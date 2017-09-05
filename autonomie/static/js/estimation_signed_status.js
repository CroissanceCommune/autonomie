/*
 * File Name : estimation_signed_status.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

var EstimationSignedStatus = {
    ui: {
        buttons: '.btn',
    },
    el: "div.signed_status_group",
    onClick: function(event){
        var value = $(event.target).find('input').val();
        ajax_request(this.url, {'submit': value}, 'POST', {success: this.refresh});
    },
    refresh: function(){
        window.location.reload();
    },
    setup: function(){
        var this_ = this;
        this.$el = $(this.el);
        this.url = this.$el.attr('data-url');
        _.each(this.ui, function(value, key){
            this_.ui[key] = this_.$el.find(value);
        });
        this.ui.buttons.on('click', _.bind(this.onClick, this));
    }
};

$(function(){
    EstimationSignedStatus.setup();
});
