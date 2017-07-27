/*
 * File Name : DiscountCollection.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Bb from 'backbone';
import DiscountModel from './DiscountModel.js';

const DiscountCollection = Bb.Collection.extend({
    model: DiscountModel,
    url: function(){
        return AppOption['context_url'] + '/' + 'discount_lines';
    }
});
export default DiscountCollection;
