/*
 * File Name : TaskLineModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import _ from 'underscore';
import Bb from 'backbone';
import { strToFloat, getTvaPart } from '../../math.js';
import BaseModel from "./BaseModel.js";

const TaskLineModel = BaseModel.extend({
    props: [
        'id',
        'order',
        'description',
        'cost',
        'quantity',
        'unity',
        'tva',
        'product_id',
        'task_id', ],
    validation: {
        description: {
            required: true,
            msg: "Veuillez saisir un objet",
        },
        cost: {
            required: true,
            pattern: "amount",
            msg: "Veuillez saisir un coup unitaire, dans la limite de 5 chiffres après la virgule",
        },
        quantity: {
            required: true,
            pattern: "amount",
            msg: "Veuillez saisir une quantité, dans la limite de 5 chiffres après la virgule",
        },
        tva: {
            required: true,
            pattern: "number",
            msg: "Veuillez sélectionner une TVA"
        },
    },
    ht: function(){
        return strToFloat(this.get('cost')) * strToFloat(this.get('quantity'));
    },
    tva_value: function(){
        var tva = this.get('tva');
        if (tva < 0){
            tva = 0;
        }
        return tva;
    },
    tva: function(){
        var val = getTvaPart(this.ht(), this.tva_value());
        return val;
    },
    ttc: function(){
        return this.ht() + this.tva();
    },
    loadProduct: function(product_datas){
        this.set('description', product_datas.label);
        this.set('cost', product_datas.value);
        this.set('quantity', 1);
        this.set('tva', product_datas.tva);
        this.trigger('set:product');
    }
});

export default TaskLineModel;
