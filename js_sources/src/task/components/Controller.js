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

const Controller = Mn.Object.extend({
    initialize: function(datas){
        this.mainView = new MainView({"datas": datas});
        App.showView(this.mainView);
    },
    status: function(status){
        this.mainView.showBox(status);
    }
});
export default Controller
