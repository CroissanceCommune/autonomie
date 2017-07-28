/*
 * File Name : TaskGroupFormView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import InputWidget from './InputWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import ModalFormBehavior from '../behaviors/ModalFormBehavior.js';
import { ajax_call, getOpt } from '../../tools.js';
import CatalogTreeView from './CatalogTreeView.js';
import LoadingWidget from './LoadingWidget.js';

var template = require('./templates/TaskGroupFormView.mustache');

const TaskGroupFormView = Mn.View.extend({
    template: template,
    regions: {
        'title': '.title',
        'description': '.description',
        'catalog_container': '#catalog-container',
    },
    ui: {
        btn_cancel: "button[type=reset]",
        form: "form",
        submit: 'button[type=submit]',
        main_tab: 'ul.nav-tabs li:first a',
    },
    behaviors: [ModalFormBehavior],
    triggers: {
        'click @ui.btn_cancel': 'modal:close'
    },
    childViewEvents: {
        'catalog:edit': 'onCatalogEdit'
    },
    childViewTriggers: {
        'catalog:insert': 'catalog:insert',
        'change': 'data:modified',
    },
    modelEvents: {
        'change': 'refreshForm'
    },
    onCatalogEdit: function(productgroup_datas){
        this.model.loadProductGroup(productgroup_datas);
    },
    isAddView: function(){
        return !getOpt(this, 'edit', false);
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            add: this.isAddView(),
        };
    },
    refreshForm: function(){
        this.showChildView(
            'title',
            new InputWidget(
                {
                    value: this.model.get('title'),
                    title: "Titre (optionnel)",
                    description: "Titre de l'ouvrage tel qu'affiché dans la sortie pdf, laissez vide pour ne pas le faire apparaître",
                    field_name: "title"
                }
            )
        );
        this.showChildView(
            'description',
            new TextAreaWidget({
                value: this.model.get('description'),
                title: "Description (optionnel)",
                field_name: "description",
                tinymce: true,
                cid: this.model.cid
            })
        );
        if (this.isAddView()){
            this.getUI('main_tab').tab('show');
        }
    },
    onRender: function(){
        this.refreshForm();
        if (this.isAddView()){
            this.showChildView(
                'catalog_container',
                new LoadingWidget()
            );
            var req = ajax_call(
                AppOption['load_catalog_url'],
                {type: 'sale_product_group'},
            );
            req.done(this.onCatalogLoaded.bind(this))
        }
    },
    onCatalogLoaded: function(result){
        this.showChildView(
            'catalog_container',
            new CatalogTreeView(
                {
                    catalog: result,
                    title: "Catalogue produit",
                }
            )
        );
    }
});
export default TaskGroupFormView;
