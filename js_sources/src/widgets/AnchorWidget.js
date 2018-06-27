/*
 * File Name : AnchorWidget.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { getOpt } from '../tools.js';
import { getPercent } from '../math.js';


const AnchorWidget = Mn.View.extend({
    tagName: 'div',
    template: require('./templates/AnchorWidget.mustache'),
    ui: {
        anchor: 'a'
    },
    events: {
        'click @ui.anchor': "onClick",
    },
    onClick() {
        var options = this.model.get('option');
        if (options.popup){
            window.openPopup(options.url);
        }
    }
});


export default AnchorWidget;
