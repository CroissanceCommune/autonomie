<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
% if addform is not None:
    <button class='btn btn-primary primary-action' data-target="#project-forms" aria-expanded="false" aria-controls="project-forms" data-toggle='collapse'>
            <i class='glyphicon glyphicon-plus'></i>
            Ajouter un projet
        </button>
        <div class='collapse row' id="project-forms">
            <div class='col-md-12 col-lg-6'>
                <h2>Ajouter un projet</h2>
                ${addform|n}
            </div>
        </div>
    <hr />
% endif
<a class="btn btn-default large-btn
    % if '__formid__' in request.GET:
        btn-primary
    % endif
    " href='#filter-form' data-toggle='collapse' aria-expanded="false" aria-controls="filter-form">
    <i class='glyphicon glyphicon-filter'></i>&nbsp;
    Filtres&nbsp;
    <i class='glyphicon glyphicon-chevron-down'></i>
</a>
% if '__formid__' in request.GET:
    <span class='help-text'>
        <small><i>Des filtres sont actifs</i></small>
    </span>
% endif
% if '__formid__' in request.GET:
    <div class='collapse' id='filter-form'>
% else:
    <div class='in collapse' id='filter-form'>
% endif
        <div class='row'>
            <div class='col-xs-12'>
<hr/>
            % if '__formid__' in request.GET:
                <a href="${request.current_route_path(_query={})}">Supprimer tous les filtres</a>
                <br />
                <br />
            %endif
                ${form|n}
            </div>
        </div>
<hr/>
    </div>
<table class="table table-striped table-condensed table-hover">
    <thead>
        <tr>
            <th class="visible-lg">${sortable(u"Créé le", "created_at")}</th>
            <th>${sortable(u"Code", "code")}</th>
            <th>${sortable(u"Nom", "name")}</th>
            <th>Clients</th>
            <th class="actions">Actions</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for id, project in records:
                <tr class='tableelement' id="${project.id}">
                    <% url = request.route_path("project", id=project.id) %>
                    <% onclick = "document.location='{url}'".format(url=url) %>
                    <td onclick="${onclick}" class="visible-lg rowlink" >${api.format_date(project.created_at)}</td>
                    <td onclick="${onclick}" class='rowlink'>${project.code}</td>
                    <td onclick="${onclick}" class='rowlink'>
                        % if project.archived:
                            <span class='label label-warning'>Ce projet est archivé</span>
                        % endif
                        ${project.name}
                    </td>
                    <td onclick="${onclick}" class='rowlink'>
                        <ul>
                            % for customer in project.customers:
                                <li>
                                ${customer.get_label()}
                                </li>
                            % endfor
                        </ul>
                    </td>
                    <td class='text-right'>
		                <div class='btn-group'>
		                    <button
                                type="button"
                                class="btn btn-default dropdown-toggle"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">
                                Actions <span class="caret"></span>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-right">
                                % for url, label, title, icon, options in stream_actions(project):
                                    ${dropdown_item(url, label, title, icon=icon, **options)}
                                % endfor
                            </ul>
                        </div>
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun projet n'a été créé pour l'instant
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(records)}
</%block>
<%block name='footerjs'>
$(function(){
        $('input[name=search]').focus();
});
</%block>
