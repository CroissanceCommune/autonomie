/*
 * File Name : FileRequirementModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import { ajax_call } from '../../tools.js';


const FileRequirementModel = Bb.Model.extend({
    label(){
        let status = this.get('status');
        let requirement_type = this.get('requirement_type');
        let file_id = this.get('file_id');
        let validation_status = this.get('validation_status');
        let forced = this.get('forced');
        let file_type = this.get('file_type');

        var label = file_type.label;
        if (status == 'danger'){
            label += ": <b>Aucun fichier n'a été fourni</b>";
        } else if (status == 'warning'){
            if (requirement_type == 'recommended'){
                label += " (recommandé)";
            } else if (validation_status != 'valid'){
                label += ": <b>Fichier en attente de validation";
            }
        } else if (forced){
            label += "La validation a été forcée";
        }
        return label;
    },
    missingFile(){
        let status = this.get('status');
        return ((status != 'success') && (!this.has('file_id')))
    },
    hasFile(){
        return this.has('file_id');
    },
    validate(){
        var serverRequest = ajax_call(
            this.url() + '?action=validation_status',
            {"validation_status": "valid"},
            "POST"
        );
        serverRequest.then(this.fetch.bind(this));
    }
});
export default FileRequirementModel;
