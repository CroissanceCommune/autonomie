/*
 * File Name : ToggleWidgetView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';

var template = require('./templates/widgets/ToggleWidgetView.mustache');

const ToggleWidgetView = Mn.View.extend({
   template:template,
   ui: {
   }
});

export default ToggleWidgetView;
