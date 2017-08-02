/*
 * File Name : TextAreaWidget.js
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

import setupTinyMce from '../../tinymce.js';

var template = require('./templates/widgets/TextAreaWidget.mustache');

const TextAreaWidget = Mn.View.extend({
    tagName: 'div',
    className: 'form-group',
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
    getTagId: function(){
        /*
         * Return an id for the current textarea
         */
        var cid = getOpt(this, 'cid', '');
        if (cid === ''){
            return false
        }
        var field_name = this.getOption('field_name');
        return field_name + "-" + cid;
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            description: this.getOption('description'),
            field_name: this.getOption('field_name'),
            value: getOpt(this, 'value', ''),
            rows: getOpt(this, 'rows', 3),
            editable: getOpt(this, 'editable', true),
            tagId: this.getTagId(),
            placeholder: getOpt(this, "placeholder", false),
        }
    },
    onAttach: function(){
        var tiny = getOpt(this, 'tinymce', false);
        if (tiny){
            var onblur = this.onBlur.bind(this);
            var onkeyup = this.onKeyUp.bind(this);
            setupTinyMce(
                {
                    selector: "#" + this.getTagId(),
                    init_instance_callback: function (editor) {
                        editor.on('blur', onblur);
                        editor.on('keyup', onkeyup);
                        editor.on('change', function () {
                            tinymce.triggerSave();
                        });
                    }
                }
            );
        }
    }
});
export default TextAreaWidget;
