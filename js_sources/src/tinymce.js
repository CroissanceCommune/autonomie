/*
 * File Name : tinymce.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

var tinymce = require('tinymce/tinymce');
const setupTinyMce = function(kwargs){
    /*
     * Setup a tinymce editor
     * kwargs are tinymce init options to be added to the default ones
     *
     * Should at least provide the selector key
     *
     * https://www.tinymce.com/docs/
     */
    tinymce.remove();
    let options = {
      body_class: 'form-control',
      theme_advanced_toolbar_location: "top",
      theme_advanced_toolbar_align: "left",
      content_css: "/fanstatic/fanstatic/css/richtext.css",
      language: "fr_FR",
      plugins: ["lists", "searchreplace visualblocks fullscreen", "paste"],
      theme_advanced_resizing: true,
      height: "100px", width: 0,
      theme: "modern",
      strict_loading_mode: true,
      mode: "none",
      skin: "lightgray",
      menubar: false,
      convert_fonts_to_spans: true,
      paste_as_text: true,
    };
    _.extend(options, kwargs);
    tinymce.init(options);
}
export default setupTinyMce;
