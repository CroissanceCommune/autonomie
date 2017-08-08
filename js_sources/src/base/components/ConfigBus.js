/*
 * File Name : ConfigBus.js
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

const ConfigBusClass = Mn.Object.extend({
    channelName: 'config',
    radioRequests: {
        'get:form_options': 'getFormOptions',
        'has:form_section': 'hasFormSection',
        'get:form_section': 'getFormSection',
        'get:form_actions': 'getFormActions',
    },
    setFormConfig(form_config){
        this.form_config = form_config;
    },
    getFormOptions(option_name){
        /*
         * Return the form options for option_name
         *
         * :param str option_name: The name of the option
         * :returns: A list of dict with options (for building selects)
         */
        console.log("FacadeClass.getFormOptions");
        return this.form_config['options'][option_name];
    },
    hasFormSection(section_name){
         /*
          *
          * :param str section_name: The name of the section
          * :rtype: bool
          */
        return _.has(this.form_config['sections'], section_name);
    },
    getFormSection(section_name){
        /*
         *
         * Return the form section description
         * :param str section_name: The name of the section
         * :returns: The section definition
         * :rtype: Object
         */
        return this.form_config['sections'][section_name];
    },
    getFormActions(){
        /*
         * Return available form action config
         */
        return this.form_config['actions'];
    },
});
const ConfigBus = new ConfigBusClass();
export default ConfigBus;
