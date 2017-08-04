/*
 * File Name : DiscountFormPopupView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import ModalBehavior from '../behaviors/ModalBehavior.js';
import DiscountFormView from './DiscountFormView.js';
import DiscountPercentModel from '../models/DiscountPercentModel.js';
import DiscountPercentView from './DiscountPercentView.js';
import { getOpt } from '../../tools.js';

var template = require('./templates/DiscountFormPopupView.mustache');

const DiscountFormPopupView = Mn.View.extend({
    behaviors: [ModalBehavior],
    template: template,
    regions: {
        'simple-form': '.simple-form',
        'percent-form': '.percent-form',
    },
    // Here we bind the child FormBehavior with our ModalBehavior
    // Like it's done in the ModalFormBehavior
    childViewTriggers: {
        'cancel:form': 'modal:close',
        'success:sync': 'modal:close',
        'insert:percent': 'insert:percent'
    },
    onModalBeforeClose(){
        this.model.rollback();
    },
    isAddView: function(){
        return !getOpt(this, 'edit', false);
    },
    onRender: function(){
        this.showChildView(
            'simple-form',
            new DiscountFormView({
                model: this.model,
                title: this.getOption('title'),
                destCollection: this.getOption('destCollection')
            })
        );

        if (this.isAddView()){
            this.showChildView(
                'percent-form',
                new DiscountPercentView(
                    {
                        title: this.getOption('title'),
                        model: new DiscountPercentModel(),
                        destCollection: this.getOption('destCollection')
                    }
                )
            );
        }
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            add: this.isAddView(),
        }
    }
});
export default DiscountFormPopupView;
