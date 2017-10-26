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
        phase: 'select[name=phase_id]'
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

        if (_.isUndefined(findone)){
            selected = projects[0].id;
        }
        var options = "";
        if (projects){
            for (var i = 0; i < projects.length; i++) {
                var project = projects[i];
                options += "<option value='" + project.id;
                if (project.id==selected){
                    options += "' selected='selected'>";
                }else{
                    options += "'>";
                }
                options += project.name + '(' + project.code + ')' + "</option>";
            }
        }
        this.ui.project.html(options);
        this.ui.project.effect('highlight', {}, 1200);
        this.ui.project.change();
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
        }
        this.ui.phase.html(options);
        this.ui.phase.effect('highlight', {}, 1200);
    },
    getProjectId: function(){
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
    toggle_project:function(value){
        if (_.isUndefined(value)){
            value = true;
        }
        this.ui.project.attr('disabled', value);
    },
    toggle_phase:function(value){
        if (_.isUndefined(value)){
            value = true;
        }
        this.ui.phase.attr('disabled', value);
    },
    customerChange: function(event){
        this.toggle_phase();
        this.toggle_project();
        var customer = this.findCustomer();
        var project_id = this.getProjectId();
        this.updateProject(customer.get('projects'), project_id);
        this.toggle_project(false);
    },
    projectChange: function(event){
        this.toggle_phase();
        var project = this.findProject();
        this.updatePhase(project.get('phases'));
        this.toggle_phase(false);
    },
    setupUi: function(){
        var this_ = this;
        this.$el = $(this.el);
        _.each(this.ui, function(value, key){
            this_.ui[key] = this_.$el.find(value);
        });
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
        this.ui.customer.change();
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
