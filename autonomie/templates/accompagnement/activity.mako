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
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/utils.mako" import="format_filelist" />
<%block name="content">
<a class='btn btn-default pull-right' href='${request.route_path("activity.pdf", id=request.context.id)}' ><i class='glyphicon glyphicon-file'></i>PDF</a>
<div class="activity-view">
<div class='row'>
    <div class='col-xs-12'>
                <% items = (\
                (u'Conseiller(s)', ','.join([api.format_account(conseiller) for conseiller in activity.conseillers])), \
                    (u'Horaire', api.format_datetime(activity.datetime)), \
                    (u"Action financée", u"%s %s" % (activity.action_label, activity.subaction_label)), \
                    (u"Nature du rendez-vous", activity.type_object.label), \
                    (u"Mode d'entretien", activity.mode), \
                    )
                %>
        ${definition_list(items)}
        <strong>Fichiers attachés</strong>
        ${format_filelist(activity)}
        <h3>Participants</h3>
        % for participant in activity.participants:
            <dl class="dl-horizontal">
                <dt>${api.format_account(participant)}</dt>
                <dd class='hidden-print'>${ format_mail(participant.email) }</dd>
            </dl>
        %endfor
        <% options = (\
                (u"Point de suivi", "point"),\
                (u"Définition des objectifs", "objectifs"), \
                (u"Plan d'action et préconisations", "action" ),\
                (u"Documents produits", "documents" ),\
                )
        %>
        % for label, attr in options:
            <h3>${label}</h3>
            ${format_text(getattr(activity, attr))}
        % endfor
    </div>
</div>
</div>
</%block>
