/*
 * File Name : BookMarkCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';

import ExpenseModel from './ExpenseModel.js';

const BookMarkCollection = Bb.Collection.extend({
    url: "/api/v1/bookmarks",
    model: ExpenseModel,
    addBookMark(model){
        let keys = [
            'ht',
            'tva',
            'km',
            'start',
            'end',
            'description',
            'type_id',
            'category'
        ];
        console.log(model);
        var attributes = _.pick(model.attributes, ...keys);
        console.log(attributes);
        this.create(attributes, {wait: true});
    },
});
export default BookMarkCollection;
