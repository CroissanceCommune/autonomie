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
import FormBehavior from '../behaviors/FormBehavior.js';
import TextAreaWidget from './TextAreaWidget.js';

var template = require("./templates/NotesBlockView.mustache");


const NotesBlockView = Mn.View.extend({
    tagName: 'div',
    className: 'form-section',
    template: template,
    regions: {
        exclusions: '.exclusions',
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
        if (this.model.get('exclusions')){
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
                description: 'Notes complémentaires concernant les prestations décrites',
                field_name: 'exclusions',
                value: this.model.get('exclusions'),
            }
        );
        this.showChildView('exclusions', view);
    }
});
export default NotesBlockView;
