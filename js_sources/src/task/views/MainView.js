/*
 * File Name : MainView.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import CommonView from "./CommonView.js";
import RightBarView from "./RightBarView.js";
import CommonModel from "../models/CommonModel.js";

const template = require('./templates/MainView.mustache');

const MainView = Mn.View.extend({
    template: template,
    regions: {
        common: '#common',
        rightbar: "#rightbar",
        footer: '#footer'
    },
    onRender: function() {
        this.commonModel = new CommonModel(
            this.getOption('datas')
        );
        this.commonModel.url = AppOption['context_url'];
        console.log(this.getOption('datas'));
        this.showChildView('common', new CommonView({model: this.commonModel}));
        this.showChildView('rightbar', new RightBarView({actions: AppOption['form_options']['actions']}));
    }
});
export default MainView;
