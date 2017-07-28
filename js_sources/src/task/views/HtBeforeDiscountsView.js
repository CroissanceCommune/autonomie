/*
 * File Name : HtBeforeDiscountsView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { formatAmount } from "../../math.js";
import LabelRowWidget from './LabelRowWidget.js';

const HtBeforeDiscountsView = Mn.View.extend({
    template: require('./templates/LineContainerView.mustache'),
    regions: {
        line: {
            el: '.line',
            replaceElement: true
        }
    },
    modelEvents: {
        'change': 'render',
    },
    onRender: function(){
        var values = formatAmount(this.model.get('ht_before_discounts'), false);
        var view = new LabelRowWidget(
            {
                label: 'Total HT avant remise',
                values: values
            }
        );
        this.showChildView('line', view);
    }
});
export default HtBeforeDiscountsView;
