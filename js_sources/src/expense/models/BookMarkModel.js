/*
 * File Name : BookMarkModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';

const BookMarkModel = Bb.Model.extend({
    initialize: function(options){
        var type_id = options['type_id'];
        if (! _.isUndefined(type_id)){
            this.set('type', this.getType(type_id));
        }
    },
    getType: function(type_id){
        return _.find(
            AppOptions['expense_types'],
            function(type){
                return type['value'] == type_id;
            }
        );
    }
});
export default BookMarkModel;
