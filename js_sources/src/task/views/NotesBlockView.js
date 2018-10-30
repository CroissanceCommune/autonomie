/*
 * File Name : NotesBlockView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import FormBehavior from '../../base/behaviors/FormBehavior.js';
import TextAreaWidget from '../../widgets/TextAreaWidget.js';

var template = require("./templates/NotesBlockView.mustache");


const NotesBlockView = Mn.View.extend({
    tagName: 'div',
    className: 'form-section',
    template: template,
    regions: {
        notes: '.notes',
    },
    behaviors: [
        {
            behaviorClass: FormBehavior,
            errorMessage: "Vérifiez votre saisie"
        }
    ],
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    isMoreSet: function(){
        if (this.model.get('notes')){
            return true;
        }
        return false;
    },
    templateContext: function(){
        return {
            is_more_set: this.isMoreSet(),
        }
    },
    onRender: function(){
        const view = new TextAreaWidget(
            {
                title: 'Notes',
                description: 'Notes complémentaires',
                field_name: 'notes',
                value: this.model.get('notes'),
            }
        );
        this.showChildView('notes', view);
    }
});
export default NotesBlockView;
