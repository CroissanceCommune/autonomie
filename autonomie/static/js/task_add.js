/*
 * * Copyright (C) 2012-2013 Croissance Commune
 * * Authors:
 *       * Arezki Feth <f.a@majerti.fr>;
 *       * Miotte Julien <j.m@majerti.fr>;
 *       * Pettier Gabriel;
 *       * TJEBBES Gaston <g.t@majerti.fr>
 *
 * This file is part of Autonomie : Progiciel de gestion de CAE.
 *
 *    Autonomie is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    Autonomie is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
 */

var AppOptions = AppOptions || {};

var ProjectModel = Backbone.Model.extend({});
var ProjectCollection = Backbone.Collection.extend({
    model: ProjectModel,
});
var CustomerModel = Backbone.Model.extend({
    initialize: function(){
        this.projects = new ProjectCollection(this.get('projects'));
    }
});
var CustomerCollection = Backbone.Collection.extend({
    model: CustomerModel,
    url: function(){
        return "/api/v1/companies/" +
            AppOptions['company_id'] +
            "/customers";
    },
});

var TaskAddProxy = {
    /*
     *
     * Handle select updates in the task add and move forms
     */
    ui: {
        customer: 'select[name=customer_id]',
        hidden_customer: 'input[name=customer_id]',
        project: 'select[name=project_id]',
        phase: 'select[name=phase_id]',
        business_type: 'select[name=business_type]',
        submit: 'button[type=submit]'
    },
    el: '#deform',
    updateProject: function(projects, current_id){
        /*
         * Update the project select
         */
        var findone = _.find(
            projects,
            function(item){return item.id == current_id;}
        );
        var selected = current_id;

        var options = "";
        if (projects && (projects.length > 0)){
            if (_.isUndefined(findone)){
                selected = projects[0].id;
            }
            for (var i = 0; i < projects.length; i++) {
                var project = projects[i];
                options += "<option value='" + project.id;
                if (project.id==selected){
                    options += "' selected='selected'>";
                }else{
                    options += "'>";
                }
                options += project.name;
                if (!_.isNull(project.code)){
                    options += ' (' + project.code + ')';
                }
                options += "</option>";
            }
            this.ui.project.html(options);
            this.ui.project.effect('highlight', {}, 1200);
            this.enableForm(true);
            // If the previously selected project is still in the list we don't
            // change
            if (_.isUndefined(findone)){
                this.ui.project.change();
            }
        } else {
            this.ui.project.html("");
            this.enableForm(false);
            this.ui.project.change();
        }
    },
    enableForm: function(value){
        this.ui.submit.attr('disabled', !value);
    },
    updatePhase: function(phases){
        var options = "";
        if (phases){
            for (var i = 0; i < phases.length; i++) {
                var phase = phases[i];
                options += "<option value='" + phase.id + "'>"  +
                    phase.name +
                    "</option>";
            }
            this.ui.phase.html(options);
            this.ui.phase.effect('highlight', {}, 1200);
        }
    },
    updateBusinessType: function(business_types){
        var options = "";
        if (business_types){
            for (var i = 0; i < business_types.length; i++) {
                var business_type = business_types[i];
                options += "<option value='" + business_type.id + "'>"  +
                    business_type.name +
                    "</option>";
            }
            this.ui.business_type.html(options);
            this.ui.business_type.effect('highlight', {}, 1200);
        }
    },
    getProjectId: function(){
        /*
         * Return the current project selected id
         */
        var current_id = this.ui.project.children('option:selected').val();
        return parseInt(current_id, 10);
    },
    findProject: function(){
        var customer = this.findCustomer();
        var current_id = this.getProjectId();
        var project = customer.projects.findWhere({id: current_id});
        return project;
    },
    getCustomerId: function(){
        var res;
        if (this.ui.customer.length > 0){
            res = this.ui.customer.children('option:selected').val();
        } else {
            res = this.ui.hidden_customer.val();
        }
        return parseInt(res, 10);
    },
    findCustomer: function(){
        var current_id = this.getCustomerId();
        var customer = this.collection.findWhere({id: current_id});
        return customer;
    },
    getPhaseId: function(){
        var current_id = this.ui.phase.children('option:selected').val();
        return parseInt(current_id, 10);
    },
    findPhase: function(){
        var project = this.findProject();
        var current_id = this.getPhaseId();
        var phase = project.phases.findWhere({id: current_id});
        return phase;
    },
    getBusinessCycleId: function(){
        var current_id = this.ui.phase.children('option:selected').val();
        return parseInt(current_id, 10);
    },
    findPhase: function(){
        var project = this.findProject();
        var current_id = this.getPhaseId();
        var phase = project.phases.findWhere({id: current_id});
        return phase;
    },
    toggle_project:function(projects){
        var value = true;
        if (! _.isUndefined(projects)){
            if (projects.length > 1){
                value = false;
            }
        }
        this.ui.project.attr('disabled', value);
    },
    toggle_phase:function(phases){
        var disabled = true;
        var visible = true;
        if (! _.isUndefined(phases)){
            if (phases.length <= 1){
                visible = false;
            } else {
                disabled = false;
            }
        }
        this.ui.phase.attr('disabled', disabled);
        this.ui.phase.parent().toggle(visible);
    },
    toggle_business_type:function(business_types){
        var disabled = true;
        var visible = true;
        if (! _.isUndefined(business_types)){
            if (business_types.length <= 1){
                visible = false;
            }
            disabled = false;
        }
        this.ui.business_type.attr('disabled', disabled);
        this.ui.business_type.parent().toggle(visible);
    },
    customerChange: function(event){
        this.toggle_phase();
        this.toggle_project();
        this.toggle_business_type();
        var customer = this.findCustomer();
        var project_id = this.getProjectId();
        var projects = customer.get('projects');
        this.updateProject(projects, project_id);
        this.toggle_project(false, projects);
    },
    projectChange: function(event){
        this.toggle_phase();
        this.toggle_business_type();
        var project = this.findProject();
        if (!_.isUndefined(project)){
            var phases = project.get('phases');
            this.updatePhase(phases);
            this.toggle_phase(phases);
            var business_types = project.get('business_types');
            this.updateBusinessType(business_types);
            this.toggle_business_type(business_types);
        } else {
            this.updatePhase([]);
            this.updateBusinessType([]);
        }
    },
    setupUi: function(){
        var this_ = this;
        this.$el = $(this.el);
        _.each(this.ui, function(value, key){
            this_.ui[key] = this_.$el.find(value);
        });
        if (this.ui.project.length > 0){
            this.ui.customer.off('change.customer');
            this.ui.customer.on(
                'change.customer',
                _.bind(this.customerChange, this)
            );
            this.ui.project.off('change.project');
            this.ui.project.on(
                'change.project',
                _.bind(this.projectChange, this)
            );
        }
        if (this.ui.phase.find('option').length == 0){
            this.toggle_phase([]);
        }
    },
    setup: function(){
        this.collection = new CustomerCollection();
        this.collection.fetch({
            success: _.bind(this.setupUi, this)
        });
    }
};

$(function(){
    TaskAddProxy.setup();
});
