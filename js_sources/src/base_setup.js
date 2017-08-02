/*
 * File Name : base_setup.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

/*
 * Setup the main ui elements
 */
import _ from 'underscore';
import $ from 'jquery';

$(function(){
    var company_menu = $('company-select-menu');
    if (!_.isNull(company_menu)){
        company_menu.on('change', function(){
            window.location = this.value;
        });
    }
    $('a[data-toggle=dropdown]').dropdown();
});
