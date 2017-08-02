/*
 * File Name : PaymentLineModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import BaseModel from "./BaseModel.js";

const PaymentLineModel = BaseModel.extend({
    props: [
        'id',
        'task_id',
        'order',
        'description',
        'amount',
        'date',
    ],
    defaults: {
        date: dateToIso(new Date()),
        order: 1,
    },
    validation: {
        description: {
            required: true,
            msg: "Veuillez saisir un objet",
        },
        amount: {
            required: true,
            pattern: "amount2",
            msg: "Veuillez saisir un montant, dans la limite de 2 chiffres après la virgule",
        },
    },
    isLast: function(){
        let order = this.get('order');
        let max_order = this.collection.getMaxOrder();
        return order == max_order;
    },
    isFirst: function(){
        let min_order = this.model.collection.getMinOrder();
        let order = this.get('order');
        return order == min_order;
    },
});

export default PaymentLineModel;
