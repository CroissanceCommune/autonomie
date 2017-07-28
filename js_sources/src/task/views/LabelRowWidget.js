/*
 * File Name : LabelRowWidget.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { getOpt } from '../../tools.js';

const LabelRowWidget = Mn.View.extend({
    tagName: 'div',
    template: require('./templates/widgets/LabelRowWidget.mustache'),
    templateContext: function(){
        var values = this.getOption('values');
        var label = getOpt(this, 'label', '');

        if (! Array.isArray(values)){
            values = [{'label': label, 'value': values}];
        }
        return {
            values: values,
        }
    }
});
export default LabelRowWidget;
