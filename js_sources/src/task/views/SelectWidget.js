/*
 * File Name : SelectWidget.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import Mn from 'backbone.marionette';
import { getOpt } from "../../tools.js";
import { updateSelectOptions } from '../../tools.js';

var template = require('./templates/widgets/SelectWidget.mustache');

const SelectWidget = Mn.View.extend({
    tagName: 'div',
    className: 'form-group',
    template: template,
    ui: {
        select: 'select'
    },
    events: {
        'change @ui.select': "onChange"
    },
    onChange: function(event){
        this.triggerMethod(
            "finish",
            this.getOption('field_name'),
            this.getUI('select').val()
        );
    },
    hasVoid(options){
        return !_.isUndefined(
            _.find(
                options,
                function(option){return option.label == '';}
            )
        );
    },
    templateContext: function(){
        var id_key = getOpt(this, 'id_key', 'value');
        var options = this.getOption('options');
        var current_value = this.getOption('value');
        var add_default = getOpt(this, 'add_default', false);
        var found_one = updateSelectOptions(options, current_value, id_key);
        if (!found_one && add_default && !this.hasVoid(options)){
            var void_option = {};
            void_option['value'] = '';
            void_option['label'] = '';
            options.unshift(void_option);
        }

        var title = this.getOption('title');
        var field_name = this.getOption('field_name');
        var multiple = getOpt(this, 'multiple', false);
        return {
            options:options,
            title: title,
            field_name: field_name,
            id_key: id_key,
            multiple: multiple
        }
    },
});
export default SelectWidget;
