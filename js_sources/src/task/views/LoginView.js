/*
 * File Name : LoginView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import ModalBehavior from '../behaviors/ModalBehavior.js';
import Radio from 'backbone.radio';

var template = require('./templates/LoginView.mustache');

const LoginView = Mn.View.extend({
    className: 'modal-overlay',
    behaviors: [ModalBehavior],
    template: template,
    url: '/api/login/v1',
    ui:{
        'form': 'form',
        'login': 'input[name=login]',
        'password': 'input[type=password]',
        'remember_me': 'input[name=remember_me]',
        'errors': '.errors',
    },
    events: {
        "submit @ui.form": "onSubmit",
    },
    onSubmit(event){
        event.preventDefault();
        this.getUI('errors').hide();
        var datas = {
            login: this.getUI('login').val(),
            password: this.getUI('password').val()
        };
        if (this.getUI('remember_me').is(':checked')){
            datas['remember_me'] = true;
        }
        var channel = Radio.channel('auth');
        channel.trigger('login', datas, this.success.bind(this), this.error.bind(this));
    },
    onModalBeforeClose(){
        console.log("Redirecting");
        window.location.replace('#');
    },
    success(){
        this.triggerMethod('close');
    },
    error(){
        this.getUI('errors').html("Erreur d'authentification");
        this.getUI('errors').show();
    }
});
export default LoginView;
