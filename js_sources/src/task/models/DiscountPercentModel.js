/*
 * File Name : DiscountPercentModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
const DiscountPercentModel = Bb.Model.extend({
    validation: {
        description: {
            required: true,
            msg: "Veuillez saisir un objet",
        },
        percentage: {
            required: true,
            range: [1, 99],
            msg: "Veuillez saisir un pourcentage",
        },
        tva: {
            required: true,
            pattern: "number",
            msg: "Veuillez sélectionner une TVA"
        },
    },

});
export default DiscountPercentModel;
