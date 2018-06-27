/*
 * File Name : FileRequirementView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import Radio from 'backbone.radio';

var template = require("./templates/FileRequirementView.mustache");

const FileRequirementView = Mn.View.extend({
    template: template,
    ui: {
        add_button: 'span.btn-add',
        view_button: "span.btn-view",
        valid_button: "button.btn-validate"
    },
    events: {
        "click @ui.add_button": "onAdd",
        "click @ui.view_button": "onView",
        "click @ui.valid_button": "onValidate"
    },
    initialize(options){
        var config_channel = Radio.channel('config');
        this.section = config_channel.request(
            'get:form_section', 'file_requirements'
        );
    },
    templateContext(){
        return {
            has_view: this.model.hasFile(),
            has_add: this.model.missingFile(),
            has_valid_link: this.model.hasFile() && this.model.get('validation') && this.section.can_validate,
            label: this.model.label()
        };
    },
    onFilePopupCallback(options){
        this.model.collection.fetch();
    },
    getCurrentUrl(){
        return window.location.href.replace('#', '').split('?')[0];
    },
    onAdd(){
        window.openPopup(
            this.getCurrentUrl() + "/addfile?file_type_id=" + this.model.get('file_type_id'),
            this.onFilePopupCallback.bind(this)
        );
    },
    onView(){
        window.openPopup(
            "/files/" + this.model.get("file_id"), this.onFilePopupCallback.bind(this)
        );
    },
    onValidate(){
        this.model.validate();
    }
});
export default FileRequirementView;
