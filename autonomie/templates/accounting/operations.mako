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
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='content'>
<a class='btn btn-primary primary-action'
    href="${request.route_path('/accounting/operation_uploads/{id}', id=request.context.id, _query={'action': 'compile'})}"
    >
    <i class='fa fa-calculator'></i> Recalculer les indicateurs issus de ces écritures
</a>
<a class='btn btn-default secondary-action'
    href="${request.route_path('/accounting/operation_uploads/{id}', id=request.context.id, _query={'action': 'delete'})}"
    onclick='return window.confirm("Ëtes-vous sûr de vouloir supprimer ces écritures, cela supprimera également tous les indicateurs générés depuis celles-ci. \nContinuer ?");'>
    <i class='glyphicon glyphicon-trash'></i> Supprimer ces écritures
</a>
<hr />

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
    <div class='help-text'>
        <a href="${request.current_route_path(_query={})}">
            <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
        </a>
    </div>
% endif
% if '__formid__' in request.GET:
    <div class='collapse' id='filter-form'>
% else:
    <div class='in collapse' id='filter-form'>
% endif
        <div class='row'>
            <div class='col-xs-12'>
<hr/>
                ${form|n}
            </div>
        </div>
<hr/>
    </div>
<div class='row'>
    <div class='col-md-4 col-md-offset-8 col-xs-12'>
        <table class='table table-bordered status-table'>
            <tr>
                <td class='operation-associated-True'><br /></td>
                <td>Écritures associées à une entreprise</td>
            </tr>
            <tr>
                <td class='operation-associated-False'><br /></td>
                <td>Écritures n'ayant pas pu être associées à une entreprise</td>
            </tr>
        </table>
    </div>
</div>
<table class="table table-condensed table-hover status-table">
    <thead>
        <tr>
            <th class="visible-lg">${sortable(u"Compte analytique", "analytical_account")}</th>
            <th class="visible-lg">${sortable(u"Compte général", "general_account")}</th>
            <th>Libellé</th>
            <th>Débit</th>
            <th>Crédit</th>
            <th>Solde</th>
        </tr>
    </thead>
    <tbody>
        % if records:
            % for entry in records:
                <tr class='tableelement operation-associated-${bool(entry.company_id)}' id='${entry.id}'>
                    <td>
                    ${entry.analytical_account}
                    </td>
                    <td>${entry.general_account}</td>
                    <td>${entry.label}</td>
                    <td>${api.format_amount(entry.debit, precision=0)|n} €</td>
                    <td>${api.format_amount(entry.credit, precision=0)|n} €</td>
                    <td>${api.format_amount(entry.balance, precision=0)|n} €</td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='4'>
                    Aucun fichier n'a été traité
                </td>
            </tr>
    % endif
    </tbody>
    </table>
${pager(records)}
</%block>
