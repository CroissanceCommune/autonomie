/* global AppOptions; */
/*
 * File Name :
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import $ from 'jquery';
import 'bootstrap/dist/js/bootstrap';
import Modal from 'bootstrap';
import _ from 'underscore';
import Bb from 'backbone';
import Mn from 'backbone.marionette';
import App from './components/App.js';
import Validation from 'backbone-validation';
import { setupBbValidationCallbacks, setupBbValidationPatterns } from '../backbone-tools.js';
import Router from './components/Router.js';
import Controller  from './components/Controller.js';
import { setupJsonRedirect, ajax_call } from '../tools.js';

setupJsonRedirect();

var template = require('../handlebars/job/file_generation.mustache');

App.on('start', function (app, options) {
    console.log("=> Starting the app");
    AppOption['form_options'] = options.form_options;
    setupBbValidationCallbacks(Validation.callbacks);
    setupBbValidationPatterns(Validation);
    var controller = new Controller(options.form_datas);
    var router = new Router({controller:controller});
    Bb.history.start();
});


$(function(){
    console.log("# Retrieving datas from the server");
    console.log(AppOption['load_url']);
    let serverCall1 = ajax_call(AppOption['load_url']);
    console.log(AppOption['context_url']);
    let serverCall2 = ajax_call(AppOption['context_url']);

    $.when(serverCall1, serverCall2).done(
        function(result1, result2){
            console.log("=> Datas retrieved");
            App.start({
                form_options: result1[0],
                form_datas: result2[0]
            });
        }
    );
})
