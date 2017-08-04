/*
 * File Name : ErrorView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';


const ErrorView = Mn.View.extend({
    tagName: 'div',
    className: 'alert alert-danger',
    template: require('./templates/ErrorView.mustache'),
    initialize(){
        this.errors = this.getOption('errors');
    },
    templateContext(){
        return {"errors": this.errors};
    }
});
export default ErrorView;
