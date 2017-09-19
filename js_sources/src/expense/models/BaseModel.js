/*
 * File Name : BaseModel.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import Radio from 'backbone.radio';
import { ajax_call } from '../../tools.js';

const BaseModel = Bb.Model.extend({
    /*
     * BaseModel for expenses, provides tools to access main options
     */
    getTypeOption(arr){
        /*
         * Retrieve the element from arr where its type_id is the same as the model's
         * current one
         */
        var type_id = this.get('type_id');
        return _.find(arr, function(type){return type['value'] == type_id;});
    },
    getTypeOptions(){
        /*
         * Return an array of options for types ( should be overriden )
         */
        return [];
    },
    getType(){
        /*
         * return the type object associated to the current model
         */
        var options = this.getTypeOptions();
        return this.getTypeOption(options);
    },
    getTypeLabel(){
        /*
         * Return the Label of the current type
         */
        var current_type = this.getType();
        var options = this.getTypeOptions();
        if (current_type === undefined){
            return "";
        }else{
            return current_type.label;
        }
    },
    rollback: function(){
        if (this.get('id') && this.url){
            this.fetch();
        }
    },
    onDuplicateError(result){
        this.collection.fetch();
        let channel = Radio.channel('message');
        channel.trigger('error:ajax', result);
    },
    onDuplicateCallback(result){
        this.collection.fetch();
        let channel = Radio.channel('message');
        channel.trigger('success:ajax', result);
    },
    duplicate(datas){
        var request = ajax_call(
            this.url() + '?action=duplicate',
            datas,
            'POST'
        );
        request.done(this.onDuplicateCallback.bind(this)
        ).fail(
            this.onDuplicateError.bind(this)
        );
        return request;
    },
});
export default BaseModel;
