/*
 * File Name : Controller.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import MainView from '../views/MainView.js';
import App from './App.js';
import Facade from './Facade.js';
import AuthBus from './AuthBus.js';
import MessageBus from './MessageBus.js';

const Controller = Mn.Object.extend({
    initialize: function(datas){
        Facade.loadModels(datas);

        AuthBus.setAuthCallbacks([Facade.syncModel]);

        AppOption.facade = Facade;
        this.mainView = new MainView();
        App.showView(this.mainView);
    },
    status: function(status){
        this.mainView.showBox(status);
    },

    login: function(){
        /*
         * Login view : show the login form
         */
        this.mainView.showLogin();
    },
});
export default Controller
