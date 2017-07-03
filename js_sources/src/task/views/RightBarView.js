/*
 * File Name : RightBarView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
var template = require("./templates/RightBarView.mustache");

const RightBarView = Mn.View.extend({
    ui: {
        buttons: 'a'
    },
    events: {
        'click @ui.buttons': 'onButtonClick'
    },
    template: template,
    templateContext: function(){
        return {
            buttons: this.getOption('actions')
        }
    },
    onButtonClick: function(event){
        console.log("Button clicked");
        console.log(this);
        console.log(event);
    }
});
export default RightBarView;
