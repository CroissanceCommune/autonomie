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
import Bb from 'backbone';


const CommonModel = Bb.Model.extend({
    props: ['altdate', 'date', 'description', 'address', 'mention_ids', 'workplace'],
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
        }
    },
    constructor: function() {
        arguments[0] = _.pick(arguments[0], this.props);
        Bb.Model.apply(this, arguments);
    }
});
export default CommonModel;
