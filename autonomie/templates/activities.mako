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
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    % if api.has_permission('manage', request.context, request):
        <a href="${request.route_path('activities', _query=dict(action='new'))}">
            Nouveau rendez-vous
        </a>
    %endif
    </li>
    <li>
    </li>
</ul>
<div class='row-fluid'>
    <div class='span7'>
        <form class='form-search form-horizontal' id='search_form' method='GET'>
            <div style="padding-bottom:3px">
                % if api.has_permission('manage', request.context, request):
                <select id='conseiller-select' name='conseiller_id' data-placeholder="Rechercher un conseiller">
                    <option value='-1'></option>
                    %for conseiller in conseiller_options:
                            <option
                                %if conseiller.id == conseiller_id:
                                    selected='1'
                                %endif
                                value='${conseiller.id}'>
                                    ${api.format_account(conseiller)}
                            </option>
                    %endfor
                </select>
                % endif
                <select name='status' id='status-select' class='span2'>
                    %for label, value in status_options:
                        <option
                            %if value == status:
                                selected='1'
                            %endif
                            value='${value}'>
                                ${label}
                            </option>
                    %endfor
                </select>
                <select name='type_id' id='type-select' class='span2' data-placeholder="Nature des Rdv">
                    <option value=-1></option>
                    %for activity_type in type_options:
                        <option
                            %if type_id == activity_type.id:
                                selected='1'
                            %endif
                            value='${activity_type.id}'>
                                ${activity_type.label}
                            </option>
                    %endfor
                </select>
                % if api.has_permission('manage', request.context, request):
                <select id='participant-select' name='participant_id' data-placeholder="Rechercher un participant" class='span3'>
                    <option value='-1'></option>
                    %for participant in participants_options:
                            <option
                            %if participant.id == participant_id:
                                    selected='1'
                                %endif
                                value='${participant.id}'>
                                    ${api.format_account(participant)}
                            </option>
                    %endfor
                </select>
                % endif
                <select class='span2' name='items_per_page' id='items-select'>
                    % for label, value in items_per_page_options:
                        % if int(value) == int(items_per_page):
                            <option value="${value}" selected='true'>${label}</option>
                        %else:
                            <option value="${value}">${label}</option>
                        %endif
                    % endfor
                </select>
            </div>
        </form>
    </div>
    <div class='span4'>
        <table class='table table-bordered'>
            <tr>
                <td class='white_tr'><br /></td>
                <td>Rendez-vous programmés</td>
            </tr>
            <tr>
                <td class='green_tr'><br /></td>
                <td>Participants présents</td>
            </tr>
            <tr>
                <td class='orange_tr'><br /></td>
                <td>Participants excusés</td>
            </tr>
            <tr>
                <td class='red_tr'><br /></td>
                <td>Participants absents</td>
            </tr>
        </table>
    </div>
</div>
</%block>
<%block name="content">
<table class="table table-condensed table-hover">
    <thead>
        <tr>
            <th>${sortable("Date", "date")}</th>
            <th>${sortable("Conseiller", "conseiller")}</th>
            <th>Participant(s)</th>
            <th>Nature du Rdv</th>
            <th>Mode de Rdv</th>
            <th style="text-align:center">Actions</th>
        </tr>
    </thead>
    <tbody>
        % for activity in records:
            <% url = request.route_path('activity', id=activity.id) %>
            <% onclick = "document.location='{url}'".format(url=url) %>
            <%
if activity.status == 'planned':
    css = "white_"
elif activity.status == 'excused':
    css = "orange_"
elif activity.status == "absent":
    css = "red_"
else:
    css = "green_"
%>
            <tr class='${css}tr'>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_date(activity.date)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${api.format_account(activity.conseiller)}
                </td>
                <td onclick="${onclick}" class="rowlink">
                    <ul>
                    % for participant in activity.participants:
                        <li>${api.format_account(participant)}</li>
                    % endfor
                    </ul>
                </td>
                <td onclick="${onclick}" class="rowlink">
                    % if activity.type_object is not None:
                        ${activity.type_object.label}
                    % endif
                </td>
                <td onclick="${onclick}" class="rowlink">
                    ${activity.mode}
                </td>
                <td>
                    % if request.user.is_contractor():
                        ${table_btn(url, u"Voir", u"Voir le rendez-vous", icon='icon-search')}
                    % else:
                        <% edit_url = request.route_path('activity', id=activity.id, _query=dict(action="edit")) %>
                        ${table_btn(edit_url, u"Voir/éditer", u"Voir / Éditer le rendez-vous", icon='icon-pencil')}
                        <% del_url = request.route_path('activity', id=activity.id, _query=dict(action="delete")) %>
                        ${table_btn(del_url, u"Supprimer",  u"Supprimer ce rendez-vous", icon='icon-delete', onclick=u"return confirm('Êtes vous sûr de vouloir supprimer ce rendez-vous ?')")}
                        <% pdf_url = request.route_path("activity.pdf", id=request.context.id) %>
                        ${table_btn(pdf_url, u"PDF", u"Télécharger la sortie PDF pour impression", icon='icon-file')}
                    %endif
                </td>
            </tr>
        % endfor
    </tbody>
</table>
</%block>
<%block name='footerjs'>
$('#conseiller-select').chosen({allow_single_deselect: true});
$('#conseiller-select').change(function(){$(this).closest('form').submit()});
$('#participant-select').chosen({allow_single_deselect: true});
$('#participant-select').change(function(){$(this).closest('form').submit()});
$('#status-select').chosen({allow_single_deselect: true});
$('#status-select').change(function(){$(this).closest('form').submit()});
$('#type-select').chosen({allow_single_deselect: true});
$('#type-select').change(function(){$(this).closest('form').submit()});
$('#items-select').chosen({allow_single_deselect: true});
</%block>
