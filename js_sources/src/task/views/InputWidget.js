/*
 * File Name : InputWidget.js
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


const InputWidget = Mn.View.extend({
    tagName: 'div',
    className: 'form-group',
    template: require('./templates/widgets/InputWidget.mustache'),
    templateContext: function(){
        return {
            value: this.getOption('value'),
            title: this.getOption('title'),
            field_name: this.getOption('field_name'),
            description: getOpt(this, 'description', false),
            type: getOpt(this, 'type', 'text')
        }
    }
});


export default InputWidget;
