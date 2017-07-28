/*
 * File Name : ModalBehavior.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';


const ModalBehavior = Mn.Behavior.extend({
  defaults: {
    modalClasses: '',
    modalOptions: {
        'keyboard': 'false',
        'backdrop': 'static'
    }
  },
  ui: {
    close: '.close'
  },
  events: {
    'hidden.bs.modal': 'triggerFinish',
    'click @ui.close': 'onClose',
  },
  onRender: function() {
    this.view.$el.addClass('modal ' + this.getOption('modalClasses'));
  },
  onAttach: function() {
    this.view.$el.modal(this.getOption('modalOptions') || {});
  },
  onClose: function(){
      console.log("Trigger cancel:form from ModalBehavior");
      this.view.triggerMethod('cancel:form');
      console.log("Trigger modal:close from ModalBehavior");
      this.view.triggerMethod('modal:close');
  },
  onModalClose: function() {
      console.log("ModalBehavior.onModalClose");
    this.view.$el.modal('hide');
  },
  triggerFinish: function() {
      console.log("Trigger destroy:modal");
    this.view.triggerMethod('destroy:modal');
  }
});
export default ModalBehavior;
