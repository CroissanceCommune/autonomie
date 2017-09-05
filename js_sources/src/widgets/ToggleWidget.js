/*
 * File Name : ToggleWidget.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { updateSelectOptions, ajax_call} from '../tools.js';

var template = require('./templates/ToggleWidget.mustache');

const ToggleWidget = Mn.View.extend({
   template:template,
   ui: {
       buttons: '.btn'
   },
   events: {
       'click @ui.buttons': 'onClick',
   },
   onClick(event){
       let url = this.model.get('options').url;
       var value = $(event.target).find('input').val();
       ajax_call(url, {'submit': value}, 'POST', {success: this.refresh});
   },
   refresh: function(){
       window.location.reload();
   },
   templateContext(){
       let buttons = this.model.get('options').buttons;

       let current_value = this.model.get('options').current_value;
       var found_one = updateSelectOptions(buttons, current_value, "status");
       console.log(buttons);
       console.log(current_value);

       return {
           name: this.model.get('options').name,
           buttons: buttons
       }
   },
});

export default ToggleWidget;
