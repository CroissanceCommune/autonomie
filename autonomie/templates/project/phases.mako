<%doc>
    * Copyright (C) 2012-2016 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
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
<%block name='mainblock'>
<div class='project-view'>
% if api.has_permission('add_phase'):
    <button class='btn btn-default secondary-action'
        data-target="#phase-form"
        aria-expanded="false"
        aria-controls="phase-form"
        data-toggle='collapse'>
        <i class='glyphicon glyphicon-plus'></i>
        Ajouter un dossier
    </button>
    <div class='collapse' id='phase-form'>
        <h3>Ajouter un dossier</h3>
        ${phase_form.render()|n}
    </div>
    <hr />
% endif

<div class='panel-group' id='phase_accordion'>
    %for phase in phases:
        %if phase.id == latest_phase_id:
            <% section_css = 'in collapse' %>
        %else:
            <% section_css = 'collapse' %>
        %endif
        <div class='panel panel-default'>
            <div class='panel-heading section-header'>
                <a href="#phase_${phase.id}"
                    data-toggle='collapse'
                    data-parent='#phase_accordion'
                    class='accordion-toggle'
                    >
                    <i style="vertical-align:middle"
                        class="glyphicon glyphicon-folder-open">
                    </i>
                    &nbsp;${phase.label()}&nbsp;
                </a>
                % if api.has_permission('edit.phase', phase):
                    <a
                        href="${request.route_path('/phases/{id}', id=phase.id)}"
                        title="Éditer le libellé de ce dossier"
                        >
                        <i style="vertical-align:middle"
                            class="glyphicon glyphicon-pencil">
                        </i>
                    </a>
                % endif
                % if api.has_permission('delete.phase', phase):
                    <a
                        href="${request.route_path('/phases/{id}', id=phase.id, _query=dict(action='delete'))}"
                        onclick="return confirm('Êtes-vous sûr de vouloir supprimer cet élément ?');"
                        title="Supprimer ce dossier"
                        >
                        <i style="vertical-align:middle"
                            class="glyphicon glyphicon-trash">
                        </i>
                    </a>
                % endif
            </div>
            <div
                class="panel-collapse ${section_css}"
                id='phase_${phase.id}'
                >
                <div class='panel-body'>
                    ${request.layout_manager.render_panel('phase_estimations', phase=phase, estimations=tasks_by_phase[phase.id]['estimations'])}
                    ${request.layout_manager.render_panel('phase_invoices', phase=phase, invoices=tasks_by_phase[phase.id]['invoices'])}
                </div>
            </div>
        </div>
    %endfor
</div>
%if not project.phases:
    <em>Aucun dossier n'a été créé dans ce projet</em>
%endif
% if tasks_without_phases is not None:
<div class='panel panel-default'>
% if phases:
    <div class='panel-heading section-header'>
    &nbsp;Documents affectés à aucun dossier
    </div>
% endif
    <div class='panel-body'>
        ${request.layout_manager.render_panel('phase_estimations', phase=None, estimations=tasks_without_phases['estimations'])}
        ${request.layout_manager.render_panel('phase_invoices', phase=None, invoices=tasks_without_phases['invoices'])}
    </div>
</div>
% endif
</div>
</%block>
<%block name="footerjs">
$( function() {
if (window.location.hash == "#showphase"){
$("#project-addphase").addClass('in');
}
});
</%block>
