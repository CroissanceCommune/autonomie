/*
 * File Name : FileRequirementCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import FileRequirementModel from './FileRequirementModel.js';


const FileRequirementCollection = Bb.Collection.extend({
    model: FileRequirementModel,
    url: function(){
        return AppOption['context_url'] + '/' + 'file_requirements';
    },
    validate(status){
        var result = true;
        this.each(function(model){
            var res = model.validate(status);
            if (! res){
                result = false;
            }
        });
        return result;
    }
});
export default FileRequirementCollection;
