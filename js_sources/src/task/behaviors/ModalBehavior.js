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
    modalOptions: null
  },

  ui: {
    close: '.close-modal'
  },
  events: {
    'hidden.bs.modal': 'triggerFinish',
  },

  triggers: {
    'click @ui.close': 'modal:close'
  },
  onRender: function() {
    this.view.$el.addClass('modal ' + this.getOption('modalClasses'));
  },
  onAttach: function() {
    this.view.$el.modal(this.getOption('modalOptions') || {});
  },
  onModalClose: function() {
    this.view.$el.modal('hide');
  },
  triggerFinish: function() {
    this.view.triggerMethod('destroy:modal');
  }
});
export default ModalBehavior;
