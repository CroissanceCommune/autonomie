/*
 * File Name : TabTotalView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Radio from 'backbone.radio';
import { formatAmount } from '../../math.js';

const TabTotalView = Mn.View.extend({
    tagName: 'div',
    template: require('./templates/TabTotalView.mustache'),
    modelEvents: {
        'change:ttc': 'render',
        'change:km_ttc': 'render',
    },
    templateContext(){
        var category = this.getOption('category');
        return {
            ttc: formatAmount(
                this.model.get('ttc_' + category) + this.model.get('km_ttc_' + category)
            )
        }
    }
});
export default TabTotalView;
