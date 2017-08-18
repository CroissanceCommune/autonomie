/*
 * File Name : ActionListView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import Mn from 'backbone.marionette';
import AnchorWidget from '../../widgets/AnchorWidget.js';
import ToggleWidget from '../../widgets/ToggleWidget.js';


const ActionListView = Mn.CollectionView.extend({
    childTemplates: {
        'anchor': AnchorWidget,
        'toggle': ToggleWidget
    },
    tagName: 'div',
    childView: function(item){
        const widget = this.childTemplates[item.get('widget')];
        if (_.isUndefined(widget)){
            console.log("Error : invalid widget type %s", item.get('widget'));
        }
        return widget;
    }
});
export default ActionListView;
