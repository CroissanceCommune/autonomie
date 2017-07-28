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
import _ from 'underscore';
import Bb from 'backbone';

const BaseModel = Bb.Model.extend({
    props: null,
    constructor: function() {
        if (!_.isNull(this.props)){
            arguments[0] = _.pick(arguments[0], this.props);
        }
        Bb.Model.apply(this, arguments);
    },
    toJSON: function(options) {
        var attributes = _.clone(this.attributes);
        if (!_.isNull(this.props)){
            attributes = _.pick(attributes, this.props);
        }
        return attributes;
    },
    rollback: function(){
        if (this.get('id')){
            this.fetch();
        }
    }
});
export default BaseModel;
