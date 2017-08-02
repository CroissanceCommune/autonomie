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

import { formatAmount } from "../../math.js";
import LabelRowWidget from './LabelRowWidget.js';

const TotalView = Mn.View.extend({
    template: require('./templates/TotalView.mustache'),
    regions: {
        ht: {
            el: '.ht',
            replaceElement: true
        },
        tvas: {
            el: '.tvas',
            replaceElement: true
        },
        ttc: {
            el: '.ttc',
            replaceElement: true
        }
    },
    modelEvents: {
        'change': 'render',
    },
    showHt: function(){
        var values = formatAmount(this.model.get('ht'), true);
        var view = new LabelRowWidget(
            {
                label: 'Total HT',
                values: values
            }
        );
        this.showChildView('ht', view);
    },
    showTvas: function(){
        var view = new LabelRowWidget({values: this.model.tva_labels()});
        this.showChildView('tvas', view);
    },
    showTtc: function(){
        var values = formatAmount(this.model.get('ttc'), true);
        var view = new LabelRowWidget(
            {
                label: 'Total TTC',
                values: values
            }
        );
        this.showChildView('ttc', view);
    },
    onRender: function(){
        this.showHt();
        this.showTvas();
        this.showTtc();
    }
});
export default TotalView;
