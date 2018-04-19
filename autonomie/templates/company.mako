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

<%doc>
    company View page
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_company" />
<%namespace file="/base/utils.mako" import="company_disabled_msg" />
<%namespace file="/base/utils.mako" import="login_disabled_msg" />
<%block name='content'>
<div class='row'>
<div class='col-md-3 col-xs-12'>
% if request.has_permission('edit_company'):
    <h3 class='text-center'>Actions</h3>
    <a
        class='btn btn-default btn-block'
        href="${request.route_path('company', id=request.context.id, _query={'action': 'edit'})}"
        ><i class='glyphicon glyphicon-pencil'></i>&nbsp;Modifier
    </a>
% endif
% if request.has_permission('admin_company'):
    % if request.context.active:
    <% label = u"Désarchiver" %>
    % else :
    <% label = u"Archiver" %>
    % endif
    <a
        class='btn btn-default btn-block'
        href="${request.route_path('company', id=request.context.id, _query={'action': 'disable'})}"
        ><i class='glyphicon glyphicon-book'></i>&nbsp;${label}
    </a>
% endif
</div>
<div class="col-md-9">
    <div class='panel panel-default page-block'>
        <div class='panel-heading'>
        Informations générales
        % if not company.active:
            ${company_disabled_msg()}
        % endif
        </div>
        <div class='panel-body'>
            <div class='row'>
                <div class='col-md-6 col-xs-12'>
                    ${format_company(company)}
                    </div><div class='col-md-6 col-xs-12'>
                    % for perm, route, label in ( \
                    ('list.estimation', 'company_estimations', u"Voir les devis"),\
                    ('list.invoice', 'company_invoices', u"Voir les factures"),\
                    ('view.commercial', 'commercial_handling', u"Voir la gestion commerciale"), \
                    ('view.treasury', '/companies/{id}/accounting/treasury_measure_grids', u"Voir les états de trésorerie"), \
                    ('list.activity', 'company_activities', u"Voir les rendez-vous"),\
                    ('list.activity', 'company_workshops', u"Voir les ateliers"),\
                    ):
                    % if request.has_permission(perm):
                    <p>
                        <a
                            href="${request.route_path(route, id=_context.id)}">
                            <i class='fa fa-arrow-right'></i>&nbsp;${label}
                        </a>
                    </p>
                    % endif
                    % endfor
                </div>
            </div>
        </div>
    </div>
    <div class='panel panel-default page-block'>
        <div class='panel-heading'>
        Employé(s)
        </div>
        <div class='panel-body'>
        % for user in company.employees:
            % if request.has_permission("view.user", user):
            <a
                href="${request.route_path('/users/{id}', id=user.id)}"
                title='Voir ce compte'>
            % endif
                <i class='glyphicon glyphicon-user'></i>&nbsp;${api.format_account(user)}
                % if user.login is not None and not user.login.active:
                ${login_disabled_msg()}
                % endif
            % if request.has_permission("view.user", user):
            </a>
            % endif
            <br />
        % endfor
        % if len(company.employees) == 0:
            Aucun entrepreneur n'est associé à cette entreprise
        % endif
        </div>
    </div>
</div>
</div>
</%block>
