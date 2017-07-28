/*
 * File Name : FormValidationBehavior.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Validation from 'backbone-validation';


const BaseFormBehavior = Mn.Behavior.extend({
    onDataPersist: function(attribute, value){
        Validation.unbind(this.view);
        Validation.bind(this.view, {
            attributes: function(view){return [attribute];}
        });

        var datas = {};
        datas[attribute] = value;
        this.view.model.set(datas);
        this.view.triggerMethod('data:persisted', datas);
    },
    onDataModified: function(attribute, value){
        Validation.unbind(this.view);
        Validation.bind(this.view, {
            attributes: function(view){return [attribute];}
        });
        var datas = {};
        datas[attribute] = value;
        this.view.model.set(datas);
        this.view.model.isValid();
    }
});
export default BaseFormBehavior;
