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


const TaskLineModel = Bb.Model.extend({
    props: [
        'id',
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
            pattern: "number",
            msg: "Veuillez saisir un coup unitaire",
        },
        quantity: {
            required: true,
            pattern: "number",
            msg: "Veuillez saisir une quantité",
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
    }
});

export default TaskLineModel;
