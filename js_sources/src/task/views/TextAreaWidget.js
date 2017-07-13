/*
 * File Name : TextAreaView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

import Mn from 'backbone.marionette';
import { getOpt } from "../../tools.js";


var template = require('./templates/widgets/TextAreaView.mustache');

const TextAreaView = Mn.View.extend({
    template: template,
    ui:{
        textarea: 'textarea'
    },
    events: {
        'keyup @ui.textarea': 'onKeyUp',
        'blur @ui.textarea': 'onBlur'
    },
    onKeyUp: function(){
        this.triggerMethod(
            'change',
            this.getOption('field_name'),
            this.getUI('textarea').val(),
        );
    },
    onBlur: function(){
        this.triggerMethod(
            'finish',
            this.getOption('field_name'),
            this.getUI('textarea').val(),
        );
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            description: this.getOption('description'),
            field_name: this.getOption('field_name'),
            value: getOpt(this, 'value', ''),
            rows: getOpt(this, 'rows', 3),
            editable: getOpt(this, 'editable', true)
        }
    }
});
export default TextAreaView;
