/*
 * File Name : FileBlockView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import FileRequirementView from './FileRequirementView.js';

var template = require("./templates/FileBlockView.mustache");


const FileCollectionView = Mn.CollectionView.extend({
    tagName: 'div',
    childView: FileRequirementView,
    collectionEvents: {
        'sync': 'render'
    }
});

const FileBlockView = Mn.View.extend({
    tagName: 'div',
    className: 'form-section',
    template: template,
    regions: {
        files: '.files',
    },
    onRender: function(){
        var view = new FileCollectionView({collection: this.collection});
        this.showChildView('files', view);
    }
});
export default FileBlockView;
