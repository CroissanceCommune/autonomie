/*
 * File Name : CheckboxListView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import $ from 'jquery';
import Mn from 'backbone.marionette';
import { getOpt } from "../../tools.js";


var template = require('./templates/widgets/CheckboxListView.mustache');

const CheckboxListView = Mn.View.extend({
    template: template,
    ui:{
        checkboxes: 'input[type=checkbox]'
    },
    events: {
        'click @ui.checkboxes': 'onClick'
    },
    getCurrentValues: function(){
        var checkboxes = this.getUI('checkboxes').find(':checked');
        var res = [];
        _.each(checkboxes, function(checkbox){
            res.push($(checkbox).attr('value'));
        });
        return res;
    },
    onClick: function(event){
        this.triggerMethod(
            'data:modified',
            this.getOption('field_name'),
            this.getCurrentValues(),
        );
    },
    templateContext: function(){
        return {
            options: this.getOption('options'),
            title: this.getOption('title'),
            description: this.getOption('description'),
            field_name: this.getOption('field_name'),
            editable: getOpt(this, 'editable', true)
        }
    }
});
export default CheckboxListView;
