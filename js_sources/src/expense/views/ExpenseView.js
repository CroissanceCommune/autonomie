/*
 * File Name : ExpenseView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { formatAmount } from '../../math.js';

const tel_template = require('./templates/ExpenseTelView.mustache');
const template = require('./templates/ExpenseView.mustache');

require("jquery-ui/ui/effects/effect-highlight");

const ExpenseView = Mn.View.extend({
    tagName: 'tr',
    ui: {
        edit: 'button.edit',
        delete: 'button.delete',
        duplicate: 'button.duplicate',
        bookmark: 'button.bookmark',
    },
    triggers: {
        'click @ui.edit': 'edit',
        'click @ui.delete': 'delete',
        'click @ui.duplicate': 'duplicate',
        'click @ui.bookmark': 'bookmark',
    },
    modelEvents: {
        'change': 'render'
    },
    getTemplate(){
        if (this.model.isSpecial()){
            return tel_template;
        } else {
            return template;
        }
    },
    highlightBookMark(){
        console.log("Highlight bookmark");
        this.getUI('bookmark').effect("highlight", {color: "#ceff99"}, "slow");
    },
    templateContext(){
        var total = this.model.total();
        var typelabel = this.model.getTypeLabel();

        return {
            edit: this.getOption('edit'),
            typelabel:typelabel,
            total:formatAmount(total),
            ht_label: formatAmount(this.model.get('ht')),
            tva_label: formatAmount(this.model.get('tva')),
        };
    }
});
export default ExpenseView;
