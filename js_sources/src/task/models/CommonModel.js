/*
 * File Name :
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import BaseModel from "./BaseModel.js";
import { strToFloat } from '../../math.js';


const CommonModel = BaseModel.extend({
    props: [
        'id',
        'altdate',
        'date',
        'description',
        'address',
        'mention_ids',
        'workplace',
        'expenses_ht',
    ],
    validation: {
        date: {
            required: true,
            msg: "Veuillez saisir une date"
        },
        description: {
            required: true,
            msg: "Veuillez saisir un objet",
        },
        address: {
            required: true,
            msg: "Veuillez saisir une adresse",
        },
        expenses_ht: {
            required: false,
            pattern: 'amount',
            msg: "Le montant doit être un nombre",
        }
    },
    ht: function(){
        return this.get('expenses_ht');
    },
    tva_key: function(){
        var result
        var tva_object = _.find(
            AppOption['tvas'],
            function(val){return val['default'];}
        );
        if (_.isUndefined(tva_object)){
            result = 0;
        } else {
            var tva = tva_object.value.toString();
            result =  strToFloat(tva);
        }
        if (result < 0){
            result = 0;
        }
        return result;
    },
    tva_amount: function(){
        return getTvaPart(this.ht(), this.tva_key());
    },
    tvaParts: function(){
        var result = {};
        var tva_amount = this.tva_key();
        result[tva_amount] = this.tva_amount();
        return result;
    },
    ttc: function(){
        return this.ht() + this.amount();
    }
});
export default CommonModel;
