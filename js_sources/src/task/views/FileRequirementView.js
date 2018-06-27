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

var template = require("./templates/FileRequirementView.mustache");

const FileRequirementView = Mn.View.extend({
    template: template,
    ui: {
        add_button: 'span.btn-add',
        view_button: "span.btn-view"
    },
    events: {
        "click @ui.add_button": "onAdd",
        "click @ui.view_button": "onView"
    },
    templateContext(){
        return {
            has_view: this.model.hasFile(),
            has_add: this.model.missingFile(),
        };
    },
    onFilePopupCallback(options){
        this.model.collection.fetch();
    },
    onAdd(){
        window.openPopup(
            window.location.href + "/addfile?file_type_id=" + this.model.get('file_type_id'),
            this.onFilePopupCallback.bind(this)
        );
    },
    onView(){
        window.openPopup(
            "/files/" + this.model.get("file_id"), this.onFilePopupCallback.bind(this)
        );
    }
});
export default FileRequirementView;
