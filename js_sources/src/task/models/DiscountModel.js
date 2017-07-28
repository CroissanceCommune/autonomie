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
import { strToFloat, getTvaPart } from '../../math.js';
import Radio from 'backbone.radio';
import BaseModel from './BaseModel.js';

const DiscountModel = BaseModel.extend({
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
    ht: function(){
        return -1 * strToFloat(this.get('amount'));
    },
    tva: function(){
        return getTvaPart(this.ht(), this.get('tva'));
    },
    ttc: function(){
        return this.ht() + this.tva();
    },
});
export default DiscountModel;
