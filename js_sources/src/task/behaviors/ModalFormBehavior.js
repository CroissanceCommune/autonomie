/*
 * File Name : ModalFormBehavior.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import {displayServerError, displayServerSuccess} from '../../backbone-tools.js';
import ModalBehavior from './ModalBehavior.js';
import FormBehavior from './FormBehavior.js';

var ModalFormBehavior = Mn.Behavior.extend({
    behaviors: [ModalBehavior, FormBehavior],
    onSuccessSync(){
        console.log("ModalFormBehavior.onSuccessSync");
        console.log("Trigger modal:close from ModalFormBehavior");
        this.view.triggerMethod('modal:close');
    },
    onModalBeforeClose(){
        console.log("Trigger reset:model from ModalFormBehavior");
        this.view.triggerMethod('reset:model');
    },
    onCancelForm(){
        console.log("ModalFormBehavior.onCancelForm");
        console.log("Trigger modal:close from ModalFormBehavior");
        this.view.triggerMethod('modal:close');
    },
    onModalClose(){
        console.log("ModalFormBehavior.onModalClose");
    }
});

export default ModalFormBehavior;
