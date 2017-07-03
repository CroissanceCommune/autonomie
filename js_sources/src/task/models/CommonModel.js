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
import Bb from 'backbone';


const CommonModel = Bb.Model.extend({
    defaults: {
        objet: "Saisissez l'objet de votre visite"
    },
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
    }
});
export default CommonModel;
