<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
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
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="definition_list" />
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name="content">
<a class='btn btn-default pull-right' href='${request.route_path("activity.pdf", id=request.context.id)}' ><i class='glyphicon glyphicon-file'></i>PDF</a>
<% activity = request.context %>
<div class='row'>
    <div class='col-md-4'>
            <% companies = set() %>
            <div class='well'>
                <h3>Participants</h3>
                <ul>
                % for participant in activity.participants:
                    <li>
                    ${api.format_account(participant)} : ${ format_mail(participant.email) }
                    </li>
                    % for company in participant.companies:
                        <% companies.add(company) %>
                    % endfor
                %endfor
                </ul>
                <h3>Activités</h3>
                % for company in companies:
                    <div>
                        <b>${company.name}</b>
                        <ul>
                        % for label, route in ( \
                        (u'Liste des factures', 'company_invoices'), \
                        (u'Liste des devis', 'estimations'), \
                            (u'Gestion commerciale', 'commercial_handling'), \
                            ):
                            <li>
                                <% url = request.route_path(route, id=company.id) %>
                                <a href='#' onclick='window.open("${url}", "${label}");'>${label}</a>
                            </li>
                        % endfor
                        </ul>
                    </div>
                % endfor
                <strong>Fichiers attachés</strong>
                ${format_filelist(activity)}
            </div>
    </div>
    <div class='col-md-8'>
            <div class='well'>
                <% items = (\
                (u'Conseiller(s)', ', '.join([api.format_account(conseiller) for conseiller in activity.conseillers])), \
                    (u'Horaire', api.format_datetime(activity.datetime)), \
                    (u'Action', u"%s %s" % (activity.action_label, activity.subaction_label)), \
                    (u"Nature du rendez-vous", activity.type_object.label), \
                    (u"Mode d'entretien", activity.mode), \
                    )\
                %>
                <div class='row'>
                    <div class='col-md-7'>
                        ${definition_list(items)}
                    </div>
                    <div class='col-md-5'>
                        <button class='btn btn-primary' data-toggle='collapse' data-target='#edition_form'>
                            Editer
                        </button>
                        <button class="btn btn-primary" data-toggle='collapse' data-target='#next_activity_form_container'>
                            Programmer un nouveau rendez-vous
                        </button>
                    </div>
                </div>

                <div
                    % if formerror is not UNDEFINED:
                        class='section-content'
                    % else:
                        class='section-content collapse'
                    % endif
                    id='edition_form'>
                    <button class="close" data-toggle="collapse" data-target='#edition_form' type="button">×</button>
                    ${form|n}
                </div>
                <div class='section-content collapse' id='next_activity_form_container'>
                    <button class="close" data-toggle="collapse" data-target='#next_activity_form_container' type="button">×</button>
                    <div id="next_activity_message"></div>
                    ${next_activity_form|n}
                </div>
            </div>
        ${record_form|n}
    </div>
</div>
<div class='row'>
    <div class="col-md-4">
    </div>
</div>
</%block>
<%block name="footerjs">
setAuthCheckBeforeSubmit('#record_form');
</%block>
