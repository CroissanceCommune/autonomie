/*
 * File Name : TotalView.js
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

const TotalView = Mn.View.extend({
    tagName: 'div',
    template: require('./templates/TotalView.mustache'),
    modelEvents: {
        'change:ttc': 'render',
        'change:ht': 'render',
        'change:tva': 'render',
        'change:km_ht': 'render',
        'change:km_tva': 'render',
        'change:km_ttc': 'render',
        'change:km': 'render',
    },
    templateContext(){
        return {
            ht: formatAmount(this.model.get('ht') + this.model.get('km_ht')),
            tva: formatAmount(this.model.get('tva') + this.model.get('km_tva')),
            ttc: formatAmount(
                this.model.get('ttc') + this.model.get('km_ttc')
            ),
            total_km: formatAmount(this.model.get('km')),
        }
    }
});
export default TotalView;
