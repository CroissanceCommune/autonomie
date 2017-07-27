/*
 * File Name : DiscountModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';

const DiscountModel = Bb.Model.extend({
    props: [
        'id',
        'amount',
        'tva',
        'ht',
        'description'
    ],
    validation: {
        description: {
            required: true,
            msg: "Veuillez saisir un objet",
        },
        amount: {
            required: true,
            pattern: "amount",
            msg: "Veuillez saisir un coup unitaire, dans la limite de 5 chiffres après la virgule",
        },
        tva: {
            required: true,
            pattern: "number",
            msg: "Veuillez sélectionner une TVA"
        },
    },
    constructor: function() {
        arguments[0] = _.pick(arguments[0], this.props);
        Bb.Model.apply(this, arguments);
    },
    ht: function(){
        return this.get('amount');
    }
});
export default DiscountModel;
