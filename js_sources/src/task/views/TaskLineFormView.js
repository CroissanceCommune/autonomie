/*
 * File Name : TaskLineFormView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import { ajax_call, getOpt } from '../../tools.js';
import {strToFloat} from '../../math.js';
import InputWidget from '../../widgets/InputWidget.js';
import SelectWidget from '../../widgets/SelectWidget.js';
import TextAreaWidget from '../../widgets/TextAreaWidget.js';
import ModalFormBehavior from '../../base/behaviors/ModalFormBehavior.js';
import CatalogTreeView from './CatalogTreeView.js';
import LoadingWidget from '../../widgets/LoadingWidget.js';
import Radio from 'backbone.radio';

var template = require('./templates/TaskLineFormView.mustache');

const TaskLineFormView = Mn.View.extend({
    template: template,
    behaviors: [ModalFormBehavior],
    regions: {
        'order': '.order',
        'description': '.description',
        'cost': '.cost',
        'quantity': '.quantity',
        'unity': '.unity',
        'tva': '.tva',
        'product_id': '.product_id',
        'catalog_container': '#catalog-container'
    },
    ui: {
        main_tab: 'ul.nav-tabs li:first a'
    },
    childViewEvents: {
        'catalog:edit': 'onCatalogEdit'
    },
    // Bubble up child view events
    //
    childViewTriggers: {
        'catalog:insert': 'catalog:insert',
        'change': 'data:modified',
        'finish': 'data:modified'
    },
    modelEvents: {
        'set:product': 'refreshForm',
        'change:tva': 'refreshProductAndVatProductSelect',
    },
    initialize: function () {
        var channel = Radio.channel('config');
        console.log('init');
        this.workunit_options = channel.request(
            'get:options',
            'workunits'
        );
        this.tva_options = channel.request(
            'get:options',
            'tvas'
        );
        this.product_options = channel.request(
            'get:options',
            'products',
        );
        this.section = channel.request(
            'get:form_section',
            'tasklines'
        );
        this.product_options = channel.request(
            'get:options',
            'products'
        );

    },
    onCatalogEdit: function(product_datas){
        this.model.loadProduct(product_datas);
    },
    isAddView: function(){
        return !getOpt(this, 'edit', false);
    },
    templateContext: function(){
        return {
            title: this.getOption('title'),
            add: this.isAddView()
        };
    },
    refreshForm: function(){
        this.showChildView(
            'order',
            new InputWidget({
                value: this.model.get('order'),
                field_name:'order',
                type: 'hidden',
            })
        );
        this.showChildView(
            'description',
            new TextAreaWidget({
                value: this.model.get('description'),
                title: "Intitulé des postes",
                field_name: "description",
                //tinymce: true, TODO Fix tinymce error
                //cid: this.model.cid
            })
        );
        this.showChildView(
            'cost',
            new InputWidget(
                {
                    value: this.model.get('cost'),
                    title: "Prix unitaire HT",
                    field_name: "cost",
                    addon: "€"
                }
            )
        );
        this.showChildView(
            'quantity',
            new InputWidget(
                {
                    value: this.model.get('quantity'),
                    title: "Quantité",
                    field_name: "quantity"
                }
            )
        );
        this.showChildView(
            'unity',
            new SelectWidget(
                {
                    options: this.workunit_options,
                    title: "Unité",
                    value: this.model.get('unity'),
                    field_name: 'unity',
                    id_key: 'value'
                }
            )
        );
        this.showChildView(
            'tva',
            new SelectWidget(
                {
                    options: this.tva_options,
                    title: "TVA",
                    value: this.model.get('tva'),
                    field_name: 'tva',
                    id_key: 'value'
                }
            )
        );
        this.showChildView(
            'product_id',
            new SelectWidget(
                {
                    options: this.product_options,
                    title: "Compte produit",
                    value: this.model.get('product_id'),
                    field_name: 'product_id',
                    id_key: 'id'
                }
            )
        );
        this.refreshProductSelect();
        if (this.isAddView()){
            this.getUI('main_tab').tab('show');
        }
    },
    getTvaIdFromValue(value){
        return _.findWhere(this.tva_options, {value: strToFloat(value)});
    },
    getDefaultTva(){
        return _.findWhere(this.tva_options, {selected: true});
    },
    getVatProductOptionsFromVatValue: function(options, val='20') {
        /*
         * Return the products list depending on tva value
         * :param string val
         */
        console.log('options', options);
        let product_options = null;
        if (! _.isUndefined(options)) {
            const currentVatProducts = _.findWhere(options, {value: Number(val)})
            if(! _.isUndefined(currentVatProducts)) {
                product_options = currentVatProducts.products;
            }
        }
        return product_options;
    },
    refreshProductAndVatProductSelect(event){
        console.log('refresh');
        this.refreshProductSelect();
        this.refreshVatProductSelect(event);
    },
    refreshVatProductSelect(event){
        /**
         * Update and show the vat products option select
         * :param string val
         */
        console.log('vat');
        const val = ! _.isUndefined(event.attributes.tva) ? event.attributes.tva : '20';
        this.product_options = this.getVatProductOptionsFromVatValue(
            this.tva_options,
            val
        );
        this.showChildView(
            'product_id',
            new SelectWidget(
                {
                    options: this.product_options,
                    title: "Compte produit",
                    value: this.model.get('product_id'),
                    field_name: 'product_id',
                    id_key: 'id'
                }
            )
        );
    },
    refreshProductSelect(){
        /*
         * Show the product select tag
         */
        if (_.has(this.section, 'product')){
            var product_options = this.product_options;

            var tva_value = this.model.get('tva');
            var tva;
            if (! _.isUndefined(tva_value)){
                tva = this.getTvaIdFromValue(tva_value);
            }
            if (!_.isUndefined(tva)){
                product_options = _.where(
                    this.product_options,
                    {tva_id: tva.id}
                );
            } else{
                var default_tva = this.getDefaultTva();
                if (!_.isUndefined(default_tva)){
                    product_options = _.where(
                        this.product_options,
                        {tva_id: default_tva.id}
                    );
                }
            }
            this.showChildView(
                'product_id',
                new SelectWidget(
                    {
                        options: product_options,
                        title: "Code produit",
                        field_name: 'product_id',
                        id_key: 'id'
                    }
                )
            );
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
                {type: 'sale_product'},
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
export default TaskLineFormView;
