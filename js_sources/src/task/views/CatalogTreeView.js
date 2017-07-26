/*
 * File Name : CatalogTreeView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { ajax_call } from "../../tools.js";

var template = require('./templates/CatalogTreeView.mustache');

const CatalogTreeView = Mn.View.extend({
    /*
     *
     * Display a jstree with the datas provided by the attribute jstree from
     * the catalog option
     *
     * :emits: catalog:selected ( <Array of ids> ) when the user submit its
     * selection
     */
    tree_options: {
        plugins: ["checkbox", 'types', "search"],
        types: {
            "default": {icon: "glyphicon glyphicon-triangle-right"},
            "product": {icon: "glyphicon glyphicon-file"},
            "group": {icon: "glyphicon glyphicon-book"}
        },
        search: {
            show_only_matches : true,
            case_insensitive: true,
        },
        core: {
            multiple: true
        }
    },
    template: template,
    ui: {
        tree: '.tree',
        search: 'input[name=catalog_search]',
        cancel_btn: 'button.cancel-catalog',
        edit_btn: 'button.edit-catalog',
        insert_btn: 'button.insert-catalog'
    },
    events: {
        'keyup @ui.search': 'onSearch',
        'click @ui.edit_btn': 'onEdit',
        'click @ui.insert_btn': 'onInsert'
    },
    onSearch: function(){
        var searchString = this.getUI('search').val();
        this.getUI('tree').jstree('search', searchString);
    },
    onAttach: function(){
        var catalog = this.getOption('catalog');
        if (_.has(catalog, "void_message")){
            this.getUI('edit_btn').prop('disabled', true);
            this.getUI('insert_btn').prop('disabled', true);
            this.getUI('search').prop('disabled', true);
            this.getUI('tree').html(catalog.void_message);
        } else {
            var tree_tag = this.getUI('tree');
            this.tree_options['core']['data'] = catalog.jstree;
            tree_tag.jstree(this.tree_options);
        }
    },
    productLoadCallback: function(result){
        this.triggerMethod("catalog:edit", result);
    },
    onEdit: function(){
        var url = null;

        var selected = this.getUI('tree').jstree('get_selected', true);
        _.each(
            selected,
            function(node){
                if (_.has(node.original, 'url')){
                    url = node.original.url;
                }
            }
        );
        if (url === null){
            alert("Veuillez sélectionner au moins un élément");
        } else {
            var serverRequest = ajax_call(url);
            serverRequest.done(this.productLoadCallback.bind(this));
        }
    },
    onInsert: function(){
        var result = [];
        var selected = this.getUI('tree').jstree('get_selected', true);
        _.each(
            selected,
            function(node){
                if (_.has(node.original, 'id')){
                    result.push(node.original.id);
                }
            }
        );
        if (result.length === 0){
            alert("Veuillez sélectionner au moins un élément");
        } else {
            this.triggerMethod('catalog:insert', result);
        }
    }
});
export default CatalogTreeView;
