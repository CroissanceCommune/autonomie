/*
 * File Name : DisplayUnitsView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import FormBehavior from "../../base/behaviors/FormBehavior.js";
import CheckboxWidget from '../../widgets/CheckboxWidget.js';

const DisplayUnitsView = Mn.View.extend({
    template: require('./templates/DisplayUnitsView.mustache'),
    fields: ['display_units'],
    behaviors: [FormBehavior],
    regions: {
        "content": "div",
    },
    childViewTriggers: {
        'change': 'data:modified',
        'finish': 'data:persist'
    },
    onRender(){
        var value = this.model.get('display_units');
        var checked = false;
        if ((value == 1)|| (value == '1')){
            checked = true;
        }
        console.log(this.model);

        this.showChildView(
            "content",
            new CheckboxWidget(
                {
                    title: "",
                    label: "Afficher le détail des prestations dans le PDF",
                    description: "Le prix unitaire et la quantité seront affichés dans le PDF",
                    field_name: "display_units",
                    checked: checked,
                    value: this.model.get('display_units'),
                }
            )
        );
    }
});
export default DisplayUnitsView;
