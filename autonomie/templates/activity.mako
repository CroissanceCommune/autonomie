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
<%block name="content">
<div class='row-fluid'>
    <div class='span8 offset2'>
                <% items = (\
                    (u'Conseiller', api.format_account(activity.conseiller)), \
                    (u'Date', api.format_date(activity.date)), \
                    (u"Nature du rendez-vous", activity.type_object.label), \
                    (u"Mode d'entretien", activity.mode), \
                    )
                %>
        ${definition_list(items)}
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
            <blockquote>
                ${format_text(getattr(activity, attr))}
            </blockquote>
        % endfor

        <h3>
    </div>
</div>

</%block>
